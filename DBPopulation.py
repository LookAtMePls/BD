from models import *
from pony.orm import *
sql_debug(True)

@db_session
def create_dishes():
    Dish(title='БигМак',
         description='Два бифштекса из 100% говядины на специальной булочке «Биг Мак», заправленной луком, двумя кусочками маринованных огурчиков, ломтиком сыра «Чеддер», салатом, и специальным соусом «Биг Мак»',
         type_of_food='Бургер',
         price='35',
         small='https://msup1.ru/img/makdonalds-menyu-zavtrak-ceny-2017-god_0.jpg',
         cover='https://2.bp.blogspot.com/-Pnn-ekI4ENc/Wt13NShD3eI/AAAAAAAAFDE/fEcS-tAPlUEWISnpjIZlhvNb5u3yoGT0ACLcBGAs/s1600/burger_mcdonalds_foodphotography_artcone.jpg',
         compiler='1')

    Dish(title='Чизбургер',
         description='Рубленый бифштекс из натуральной цельной говядины с кусочками сыра «Чеддер» на карамелизованной булочке, заправленной горчицей, кетчупом, луком и кусочком маринованного огурчика.',
         type_of_food='Бургер',
         price='25',
         small='http://www.sud67.ru/photos/min/7381_9565agrand-chizburger.jpg',
         cover='https://i.ytimg.com/vi/xlUQuu0fhh0/maxresdefault.jpg',
         compiler='1')

    Dish(title='Гамбургер',
         description='Булочка без кунжута, которую подрумянили в тостере. Рубленый бифштекс из говядины, жареный на гриле Кетчуп томатный Соус горчичный Лук репчатый резаный Огурцы маринованные Приправа для гриля специальная',
         type_of_food='Бургер',
         price='15',
         small='https://icon2.kisspng.com/20180328/ive/kisspng-mcdonald-s-hamburger-cheeseburger-mcdonald-s-quart-hamburger-5abb6c6c8f1ac7.3023431115222324285862.jpg',
         cover='https://avatars.mds.yandex.net/get-pdb/1613226/6b812e24-28ad-4447-a31b-af6adee8c7b6/s1200',
         compiler='1')

    Dish(title='Картошка Фри',
         description='Вкусные, обжаренные в растительном фритюре и слегка посоленные палочки картофеля.',
         type_of_food='Картошка',
         price='10',
         small='https://img1.pngindir.com/20180208/kuq/kisspng-mcdonalds-french-fries-fast-food-junk-food-mcdonald-s-fries-5a7ca828428f99.2808304015181189522726.jpg',
         cover='https://avatars.mds.yandex.net/get-pdb/1613226/6b812e24-28ad-4447-a31b-af6adee8c7b6/s1200',
         compiler='1')

    Dish(title='Coca-cola',
         description='Прохладительный газированный напиток.',
         type_of_food='Напиток',
         price='10',
         small='http://4.bp.blogspot.com/-tLWcMwBFWmc/Tc2sTngi9eI/AAAAAAAAAFo/3IZ8SSAb9VI/s200/mcdonalds.jpg',
         cover='http://dostavkamsk.ulcraft.com/uploads/s/7/g/p/7gp5u8lrssn7/img/full_9Lo3kYkt.jpg',
         compiler='1')

    Dish(title='Фиш Ролл',
         description='Обжаренная рыбная котлета в панировке, свежий салат, ломтики помидора и огурца, и сыр в пресной пшеничной лепешке, заправленной специальным соусом.',
         type_of_food='Ролл',
         price='15',
         small='https://time-lunch.ru/main/wp-content/uploads/2017/04/%D1%84%D0%B8%D1%88-%D1%80%D0%BE%D0%BB%D0%BB-150x150.jpg',
         cover='https://eaty-food.ru/wp-content/uploads/2019/03/eaty-63-1-1200x799.jpg',
         compiler='1')

@db_session
def create_useres():
    User(login='admin', email='lolo@mail.ru', pwd='12345', is_compiler=True, money='0')
    User(login='admin1',email='lolo1@mail.ru',pwd='12345',is_compiler=True, money='10')
    User(login='axenoff',email='lololo@mail.ru',pwd='12345',is_compiler=False, money='0')
    User(login='miha',email='lolo1o@mail.ru',pwd='12345',is_compiler=False, money='0')

def main():
    db.generate_mapping(create_tables=True)
    create_useres()
    create_dishes()


if __name__ == '__main__':
    main()
