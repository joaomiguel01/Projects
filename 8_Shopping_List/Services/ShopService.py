from ..Repositories.ShopRepository import ShopRepository
from ..Models.Shopping import Shopping

class ShopService:
    def __init__(self, shop_repo: ShopRepository):
        self._shop_repo = shop_repo
    

    def add_shop(self, name: str, quantity: int) -> Shopping:
        return self._shop_repo.create(name, quantity)
    
    def get_all_shops(self) -> list[Shopping]:
        return self._shop_repo.read_all()
    
    def update_shop(self, shop: Shopping) -> bool:
        return self._shop_repo.update(shop)
    
    def delete_shop(self, shop_id: str) -> bool:
        return self._shop_repo.delete(shop_id)