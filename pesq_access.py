from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import pandas as pd
from tabulate import tabulate

class PesqAccess:

    def __init__(self, parameters):

        self.parameters = parameters

    def request_table(self):

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        driver.get(self.parameters['root']+self.parameters['stats_path'])
        sleep(self.parameters['time_sleeping']['main_page'])

        # ipt_cod = driver.find_element(By.ID, 'formPesquisa:j_id_1m')
        ipt_cod = driver.find_element(By.ID, self.parameters.get('html_search').get('input_code_id'))
        ipt_cod.send_keys(self.parameters['stats_code'])

        # Select the SEARCH button to push
        ipt_search = driver.find_element(By.ID, self.parameters.get('html_search').get('search_btn_id'))
        ipt_search.click()
        sleep(self.parameters['time_sleeping']['query_result'])

        # Select the table
        table = driver.find_element(By.ID, self.parameters.get('html_search').get('table_result_id'))

        dataset=[]
        for row in table.find_elements(By.CSS_SELECTOR, 'tr'):
            line=list()
            for cell in row.find_elements(By.TAG_NAME, 'td'):
                line.append(cell.text)
            # create df append lists
            dataset.append(line)

        for obj in dataset:
            if 'Nenhum registro encontrado!' in obj:
                return 'Nenhum registro encontrado!'

        columns=['Id', 'Empresa', 'Codigo', 'Nome', 'Data',	'Cobertura', 'Acoes']
        df = pd.DataFrame(
            dataset,
            columns=columns
        )
        df = df.iloc[1:, :-1]
        
        return f'```\n{self.treat_table(df)}```'
    
    def treat_table(self, data):

        data['Empresa'] = data['Empresa'].str.split('/', n=1, expand=True)[1]
        data['Ano'] = data['Data'].str[-4:]
        data = data.groupby(by=["Empresa", "Ano"]).size().reset_index(name="N")

        tab = tabulate(
                data,
                headers=data.columns,
                floatfmt=".5f",
                showindex=False,
                tablefmt="psql",
            )
        
        return tab