from ..Models.Shopping import Shopping
import os
import json

class ShopRepository:
    def __init__(self, db_name: str="shop_list.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._db_name = os.path.join(base_dir, db_name)

        if not os.path.exists(self._db_name):
            with open(self._db_name, "x", encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)
    
    
    def grab_data(self) -> list[dict]:
        with open(self._db_name, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def save_data(self, data: list[dict]) -> None:
        with open(self._db_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    

    def create(self, name: str, quantity: int) -> Shopping:
        shops = self.grab_data()

        shop = Shopping(name=name, quantity=quantity)
        
        shops.append(shop.to_dict())
        self.save_data(shops)

        return shop
    
    def read_all(self) -> list[Shopping]:
        shops = self.grab_data()

        return [Shopping.from_dict(s) for s in shops]
    
    def read_by_id(self, shop_id: str) -> Shopping | None:
        shops = self.grab_data()

        for s in shops:
            if s["shop_id"] == shop_id:
                return Shopping.from_dict(s)
            
        return None
    
    def update(self, shop: Shopping) -> bool:
        shops = self.grab_data()

        for i, s in enumerate(shops):
            if s["shop_id"] == str(shop.shop_id):
                shops[i] = shop.to_dict()
                self.save_data(shops)
                return True
        
        return False
    
    def delete(self, shop_id: str) -> bool:
        shops = self.grab_data()

        new_shops = [s for s in shops if s["shop_id"] != shop_id]

        if len(shops) == len(new_shops):
            return False
        
        self.save_data(new_shops)
        return True
        
        
        