from typing import Annotated

from beanie.operators import In
from fastapi import APIRouter, HTTPException, Query, status
from beanie import PydanticObjectId
from fastapi_pagination import Page

from auth import CurrentUserType
from db.documents import Snapshot
from db.server import Product
from models.products import CreateProduct, PatchProduct, SearchProduct
from fastapi_pagination.ext.beanie import apaginate

router = APIRouter(prefix="/api/products")

type SearchTerms = Annotated[SearchProduct, Query()]

@router.get(
    "/get/{product_id}",
    response_model=Product|None
)
async def get_product_by_id(product_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(product_id)

    product = await Product.find_one(
        Product.id == object_id,
        Product.user_id == current_user.id
    )

    return product


@router.get(
    "/all",
    response_model=Page[Product]
)
async def get_all_products(
    current_user: CurrentUserType,
    search_terms: SearchProduct = Query()
):
    return apaginate(Product.find_many(
        Product.user_id == current_user.id,
        search_terms.model_dump(exclude_none=True)
    ))

@router.post(
    "/create",
    response_model=Product
)
async def create_new_product(product_data: CreateProduct, current_user: CurrentUserType):
    if not current_user.id: return None

    product = Product(
        user_id=current_user.id,
        name=product_data.name,
        brand=product_data.brand,
        description=product_data.description,
        descriptors=product_data.descriptors,
        code=product_data.code,
        life_cicle=product_data.life_cicle,
        quantity=product_data.quantity,
        measurement=product_data.measurement,
        tags=product_data.tags
    )

    return await product.insert()


@router.post(
    "/update/{product_id}",
    response_model=Product
)
async def update_product(
    product_id: str,
    product_data: PatchProduct,
    current_user: CurrentUserType
):
    object_id = PydanticObjectId(product_id)

    product = await Product.find_one(
        Product.id == object_id,
        Product.user_id == current_user.id
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot update product: product could not be found."
        )

    return await product.set(
        product_data.model_dump(exclude_unset=True)
    )


@router.delete(
    "/delete/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(product_id: str, current_user: CurrentUserType):
    object_id = PydanticObjectId(product_id)

    product = await Product.find_one(
        Product.id == object_id,
        Product.user_id == current_user.id
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete product: product could not be found."
        )

    await Snapshot.find_many(Snapshot.product_id == product.id).delete_many()

    await product.delete()

@router.delete(
    "/delete/all",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_all_products(
    current_user: CurrentUserType,
    search_terms: SearchTerms = SearchProduct()
):
    products = await Product.find_many(
        Product.user_id == current_user.id,
        search_terms.model_dump(exclude_none=True)
    ).to_list()

    product_ids = [product.id for product in products if product.id]

    if not product_ids:
        return

    await Snapshot.find_many(
        In(Snapshot.product_id, product_ids)
    ).delete_many()

    await Product.find_many(
        In(Product.id, product_ids)
    ).delete_many()