class Product:
    next_number = 1
    def __init__(self, name, price, stock):
        self.number = Product.next_number
        Product.next_number += 1
        self.name = name
        self.price = price
        self.__stock = stock
        
    def get_stock(self):
        return self.__stock
    
    def decrease_stock(self, qty):
        if qty > self.__stock:
            print("재고가 모자람 ㅡㅡ")
            return
        self.__stock -= qty
        
    def line_text(self):
        if self.__stock == 0:
            stock_text = "(품절)"
        else:
            stock_text = f"(재고 {self.__stock})"
        return f"{self.number}. {self.name}\t{self.price:,}원  {stock_text}"
    
class CartLine:
    def __init__(self, item, qty):
        self.item = item
        self.qty = qty
        
    def sub_total(self):
        return self.item.price * self.qty

class Cart:
    def __init__(self):
        self.lines = []
        self.coupon = Discount()
        
    # def find_line
    def find_line(self, item):
        for line in self.lines:
            if line.item is item:
                return line
        return None
    
    # def add_cart
    def add_cart(self, item, qty):
        line = self.find_line(item)
        in_cart = line.qty if line else 0
        can_add = item.get_stock() - in_cart
        
        if qty > can_add:
            print("재고가 부족합니다.")
            return
        
        if line:
            line.qty += qty
        else:
            self.lines.append(line)
        print(f"{item.name}이 {qty}개 추가되었습니다.")
    
    # def remove_cart
    def remove_cart(self, item):
        line = self.find_line(item)
        
        if line is None:
            print("삭제할 상품이 없습니다.")
            return
        self.lines.remove(line)
    # def total_cart 
    def total_cart(self):
        return sum([line.sub_total() for line in self.lines])