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
            print("재고보다 많이 줄일 수 없습니다.")
            return
        self.__stock -= qty
        
    def line_text(self):
        if self.__stock == 0:
            stock_text = "(품절)"
        else:
            stock_text = f"(재고 {self.__stock}개)"
        return f"{self.number}. {self.name}\t{self.price:,}원  {stock_text}"
    
class CartLine:
    def __init__(self, item, qty): 
        self.item = item # 상품 객체를 가리키게 될 것
        self.qty = qty # 담은 수량(재고와 별개)
        
    def subtotal(self):
        return self.item.price * self.qty
    
class Cart:
    def __init__(self):
        self.lines = [] # CartLine 객체들
        self.coupon = Discount() # 처음엔 쿠폰 없음
        
    # 이 상품이 담긴 줄 찾기(이미 담긴 상품이 있는지 루프로 탐색)
    def find_line(self, item): 
        for line in self.lines:
            if line.item is item: # 여기서 오른쪽 item 은 추가할 item을 의미
                return line
        return None
    
    def add(self, item, qty): # 장바구니 담기
        line = self.find_line(item)
        in_cart = line.qty if line else 0 # 이미 담은 수량
        can_add = item.get_stock() - in_cart # 재고 - 이미 담은 수량
        if qty > can_add:
            print(f"재고가 부족합니다. (담을 수 있는 수량: {can_add}개)")
            return
        if line:
            line.qty += qty # 이미 있으면 수량만 더함
        else:
            self.lines.append(CartLine(item, qty)) # 실질적인 담기 코드
        print(f"{item.name} {qty} 개를 담았습니다.")
        
    def remove(self, item):
        line = self.find_line(item)
        if line is None:
            print("장바구니에 없는 상품입니다.")
            return
        self.lines.remove(line)
        
    def item_total(self):
        return sum([line.subtotal() for line in self.lines])

    def discount(self): # 할인 (쿠폰 종류는 묻지 않음)
        return self.coupon.discount_amount(self.item_total())

    def shipping_fee(self): # 배송비
        if len(self.lines) == 0:
            return 0
        if self.item_total() - self.discount() >= 30000:
            return 0
        return 3000

    def pay_amount(self): # 결제 금액
        return self.item_total() - self.discount() + self.shipping_fee()

    def show(self):
        print("-" * 40)
        for line in self.lines:
            print(f"{line.item.name}\tx {line.qty}\t{line.subtotal():>10,}원")
        print("-" * 40)
        print(f"상품 합계\t\t{self.item_total():>10,}원")
        print(f"할인\t\t\t{-self.discount():>10,}원  [{self.coupon.name}]")
        print(f"배송비\t\t\t{self.shipping_fee():>10,}원")
        print(f"결제 금액\t\t{self.pay_amount():>10,}원")
        print("-" * 40)

    def checkout(self):
        if len(self.lines) == 0:
            print("장바구니가 비어 있습니다.")
            return
        print("[영수증]")
        self.show()
        for line in self.lines:
            line.item.decrease_stock(line.qty) # 재고는 결제할 때만 줄어든다
        self.lines = [] # 장바구니 비우기
        self.coupon = Discount() # 쿠폰 초기화
        print("결제가 완료되었습니다. 감사합니다!")
    
    
class Discount: # 부모: 쿠폰 없음
    name = "쿠폰 없음" # 클래스 변수
    
    def discount_amount(self, total):
        return 0
    
class RateDiscount(Discount): # 상속
    def __init__(self, rate, max_amount):
        # super().__init__()
        self.rate = rate
        self.max_amount = max_amount
        self.name = f"{int(rate * 100)}% 할인 (최대 {max_amount:,}원)"
    
    def discount_amount(self, total): # 오버라이딩
        amount = int(total * self.rate) # 원 단위 미만 버림
        return min(amount, self.max_amount)
    
class FixedDiscount(Discount): # 상속
    def __init__(self, amount, min_total):
        self.amount = amount
        self.min_total = min_total
        self.name = f"{amount:,}원 할인 ({min_total:,}원 이상 구매 시)"

    def discount_amount(self, total): # 오버라이딩
        if total >= self.min_total:
            return self.amount
        return 0