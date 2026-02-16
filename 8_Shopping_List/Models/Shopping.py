from uuid import UUID, uuid4

class Shopping:
    def __init__(self, name: str, quantity: int, shop_id: UUID | None=None):
        self._shop_id = shop_id or uuid4()
        self.name = name
        self.quantity = quantity


    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, name: str) -> None:
        if not (isinstance(name, str) and name.strip()):
            raise ValueError("The name can't be a blank string!")
        
        self._name = name.upper().strip()
    
    @property
    def quantity(self) -> int:
        return self._quantity
    @quantity.setter
    def quantity(self, q: int) -> None:
        if not isinstance(q, int):
            raise ValueError("The quantity must be a int instance!")
        
        if q <= 0:
            raise ValueError("The quantity must be greater than 0!")
        
        self._quantity = q
    
    @property
    def shop_id(self) -> UUID:
        return self._shop_id
    

    def to_dict(self) -> dict:
        return {
            "shop_id": str(self.shop_id),
            "name": self.name,
            "quantity": self.quantity
        }
    
    @classmethod
    def from_dict(cls, data) -> "Shopping":
        return cls(
            name=data["name"],
            quantity=int(data["quantity"]),
            shop_id=UUID(data["shop_id"])
        )
    

    def __str__(self):
        return f"Name: {self.name} | Quantity: {self.quantity}"
    
    def __repr__(self):
        return f"({self.name}, {self.quantity})"