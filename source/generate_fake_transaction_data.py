import faker
import random
import json

faker_ = faker.Faker()


def generate_fake_sales_data(num_of_data: int):

    list_of_data = []

    for _ in range(num_of_data):

        product_id = random.randint(1, 15)
        customer_id = random.randint(1, 1000)
        cogs = random.uniform(1, 1000)
        quantity = random.randint(1, 10)
        unit_sale_price = random.uniform(cogs+10, 1200)

        single_item = {
                "product_id":product_id,
                "customer_id":customer_id,
                "cogs":cogs,
                "quantity":quantity,
                "unit_sale_price": unit_sale_price
                }
        list_of_data.append(single_item)

    return list_of_data


if __name__ == "__main__":

    with open("fake.json",'w') as file:
        json.dump(generate_fake_sales_data(100), file, indent=4 )


        



