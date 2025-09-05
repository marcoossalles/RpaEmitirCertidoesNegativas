import sqlite3
import pandas as pd
from datetime import datetime
import os
from manager_logs.logger_manager import Logger

class DbServices:
    def __init__(self):
        self.logging = Logger("EmissaoCertidao")
        self.conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
        self.cursor = self.conn.cursor()

    def criar_tabela(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            cnpj TEXT NOT NULL UNIQUE,
            status TEXT,
            cidade TEXT,
            receita_federal TEXT,
            estadual TEXT,
            municipal_cae TEXT,
            municipal_certidao TEXT,
            fgts TEXT,
            trabalhista TEXT,
            status_processamento TEXT
        )
        ''')
        self.conn.commit()

    def inserir_empresas(self,empresas):
        """Insere lista de empresas, ignorando duplicatas"""
        self.logging.info("Inserindo empresas no banco de dados, ignorando duplicatas.")
        for empresa in empresas:
            self.cursor.execute('''
                INSERT OR IGNORE INTO Empresas
                (empresa, cnpj, status, cidade, receita_federal, estadual,
                municipal_cae, municipal_certidao, fgts, trabalhista, status_processamento)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    empresa['EMPRESA'].strip(),
                    empresa['CNPJ'],
                    empresa['STATUS'],
                    empresa['CIDADE'],
                    empresa['RECEITA FEDERAL'],
                    empresa['SEFAZ'],
                    empresa['MUNICIPAL']['CAE'],
                    empresa['MUNICIPAL']['CERTIDAO MUN'],
                    empresa['FGTS'],
                    empresa['TRABALHISTA'],
                    empresa['STATUS PROCESSAMENTO']
                ))
        self.conn.commit()

    def atualizar_empresa(self, cnpj, dados: dict):
        self.logging.info(f"Atualizando empresa com CNPJ: {cnpj}")

        query = 'UPDATE Empresas SET '
        updates = []
        params = []

        for coluna, valor in dados.items():
            updates.append(f"{coluna} = ?")
            params.append(valor)

        query += ', '.join(updates) + ' WHERE cnpj = ?'
        params.append(cnpj)

        self.cursor.execute(query, tuple(params))
        self.conn.commit()

    def buscar_pendentes(self):
        self.logging.info("Buscando empresas pendentes no banco de dados.")
        self.cursor.execute('''
        SELECT * FROM Empresas
        WHERE status_processamento = '' 
        OR status_processamento = 'PROCESSO PENDENTE'
        ''')
        colunas = [desc[0] for desc in self.cursor.description]  # nomes das colunas
        rows = self.cursor.fetchall()
        return [dict(zip(colunas, row)) for row in rows]

    def gerar_relatorio(self, path):
        # pega dados do banco
        df = pd.read_sql_query('SELECT * FROM Empresas', self.conn)

        # pega mês e ano atuais em PT-BR
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março",
            4: "Abril", 5: "Maio", 6: "Junho",
            7: "Julho", 8: "Agosto", 9: "Setembro",
            10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        agora = datetime.now()
        nome_aba = f"{meses[agora.month]} {agora.year}"

        # grava direto na aba do mês
        with pd.ExcelWriter(path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=nome_aba, index=False)

        self.conn.close()
