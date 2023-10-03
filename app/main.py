import requests
from bs4 import BeautifulSoup

from utils import CSVWriter, SQLiteWriter


def get_page_content(page: int, size: int = 100) -> str:
    query_parameters = {
        'indexName': 'auto,order_auto,newauto_search',
        'categories.main.id': '1',
        'country.import.usam.not': '-1',
        'price.currency': '1',
        'abroad.not': '0',
        'custom.not': '1',
        'page': page,
        'size': size,
    }
    response = requests.get('https://auto.ria.com/uk/search/', params=query_parameters)
    response.raise_for_status()
    return response.text


def main():

    headers = ['car_id', 'car_mark_name', 'data_link_to_view']

    writers = (
        CSVWriter('cars1.csv', headers),
    )
    sql = f'''
    CREATE TABLE cars(
    '{headers[0]}',
    '{headers[1]}',
    '{headers[2]}'
    );
    '''
    table = SQLiteWriter(sql)
    page = 0

    while True:
        if page == 3:
            break
        print(f'page: {page}')
        page += 1
        page_content = get_page_content(page)

        soup = BeautifulSoup(page_content, 'html.parser')

        search_results = soup.find('div', {'id': 'searchResults'})
        ticket_items = search_results.find_all('section', {'class': 'ticket-item'})

        if not ticket_items:
            break

        for ticket_item in ticket_items:
            car_details = ticket_item.find('div', {'class': 'hide'})
            car_id = car_details['data-id']
            data_link_to_view = car_details['data-link-to-view']
            car_mark_name = car_details['data-mark-name']
            data = [car_id, car_mark_name, data_link_to_view]

            for writer in writers:
                writer.write_row(data)

            sql = f"""
            INSERT INTO cars
            VALUES ('{data[0]}', '{data[1]}', '{data[2]}');
            """
            table.commit_sql(sql)


if __name__ == '__main__':
    main()
