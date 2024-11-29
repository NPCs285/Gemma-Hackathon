import psycopg2
from psycopg2.extras import RealDictCursor
import ollama
from decimal import Decimal
from typing import List, Dict, Any
from datetime import datetime
import os
from dotenv import load_dotenv

class PostgresInsightsAgent:
    def __init__(self):
        """Initialize database connection using environment variables"""
        load_dotenv()  # Load environment variables from .env file
        
        self.db_config = {
            'dbname': os.getenv('DB_NAME', 'tracker'),  # Changed default to 'tracker'
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'postgres'),  # Changed default to 'postgres'
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        if not self.db_config['password']:
            raise ValueError("Database password not found in environment variables")
            
        self.model_name = 'insights'
        self.conn = None
        
    def connect(self):
        """Establish database connection"""
        try:
            if self.conn is None or self.conn.closed:
                print(f"Connecting to database {self.db_config['dbname']} on {self.db_config['host']}...")
                self.conn = psycopg2.connect(**self.db_config)
                print("Successfully connected to database")
            return True
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            return False

    def get_transactions(self, limit: int = 100) -> List[Dict]:
        """Fetch transactions from PostgreSQL database"""
        if not self.connect():
            return []
            
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        id,
                        remarks,
                        amount::numeric::float8,
                        transaction_date,
                        category
                    FROM transactions
                    WHERE transaction_date IS NOT NULL
                    ORDER BY transaction_date DESC
                    LIMIT %s
                """, (limit,))
                
                transactions = cur.fetchall()
                return [dict(tx) for tx in transactions]
                
        except psycopg2.Error as e:
            print(f"Query error: {e}")
            return []
        finally:
            self.conn.close()
            self.conn = None

    def get_transaction_stats(self) -> Dict:
        """Get statistical summary of transactions"""
        if not self.connect():
            return {}
            
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        COUNT(*) as total_transactions,
                        SUM(amount) as total_amount,
                        AVG(amount) as avg_amount,
                        MAX(amount) as max_amount,
                        MIN(amount) as min_amount,
                        COUNT(DISTINCT category) as category_count
                    FROM transactions
                    WHERE transaction_date IS NOT NULL
                """)
                return dict(cur.fetchone())
        except psycopg2.Error as e:
            print(f"Stats query error: {e}")
            return {}
        finally:
            self.conn.close()
            self.conn = None

    def get_category_summary(self) -> List[Dict]:
        """Get summary by category"""
        if not self.connect():
            return []
            
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        COALESCE(category, 'Uncategorized') as category,
                        COUNT(*) as transaction_count,
                        SUM(amount) as total_amount,
                        AVG(amount) as avg_amount
                    FROM transactions
                    GROUP BY category
                    ORDER BY total_amount DESC
                """)
                return [dict(row) for row in cur.fetchall()]
        except psycopg2.Error as e:
            print(f"Category summary error: {e}")
            return []
        finally:
            self.conn.close()
            self.conn = None

    def format_transactions(self, transactions: List[Dict], include_stats: bool = True) -> str:
        """Format transactions and statistics for LLM analysis"""
        if not transactions:
            return "No transactions found."
            
        summary = "Recent Transactions:\n\n"
        for tx in transactions:
            date_str = tx['transaction_date'].strftime('%Y-%m-%d') if tx['transaction_date'] else 'No date'
            summary += (
                f"Date: {date_str}\n"
                f"Amount: ${float(tx['amount']):.2f}\n"
                f"Category: {tx['category'] or 'Uncategorized'}\n"
                f"Description: {tx['remarks']}\n"
                f"---\n"
            )

        if include_stats:
            stats = self.get_transaction_stats()
            if stats:
                summary += "\nOverall Statistics:\n"
                summary += f"Total Transactions: {stats['total_transactions']}\n"
                summary += f"Total Amount: ${float(stats['total_amount']):.2f}\n"
                summary += f"Average Transaction: ${float(stats['avg_amount']):.2f}\n"
                summary += f"Largest Transaction: ${float(stats['max_amount']):.2f}\n"
                summary += f"Smallest Transaction: ${float(stats['min_amount']):.2f}\n"

            category_stats = self.get_category_summary()
            if category_stats:
                summary += "\nCategory Summary:\n"
                for cat in category_stats:
                    summary += (
                        f"{cat['category']}:\n"
                        f"  Count: {cat['transaction_count']}\n"
                        f"  Total: ${float(cat['total_amount']):.2f}\n"
                        f"  Average: ${float(cat['avg_amount']):.2f}\n"
                    )
        
        return summary

    def get_insights(self, query: str, transaction_limit: int = 100) -> str:
        """Generate insights based on user query"""
        transactions = self.get_transactions(transaction_limit)
        if not transactions:
            return "No transactions available for analysis."
        
        context = self.format_transactions(transactions)
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=f"""
                    Analyze these transactions and answer this question: {query} {context}. 
                    Please provide detailed insights based on the transaction data shown above. 
                    Focus on specific numbers and trends when relevant.
                """
            )
            return response['response']
        except Exception as e:
            return f"Error generating insights: {e}"

def main():
    # Create .env file with database credentials if it doesn't exist
    env_content = """
        DB_NAME=tracker
        DB_USER=postgres
        DB_PASSWORD=postgres
        DB_HOST=localhost
        DB_PORT=5432
    """

    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("Created .env file with default credentials.")

    try:
        agent = PostgresInsightsAgent()
        print("PostgreSQL Transaction Insights Agent")
        print("====================================")
        
        while True:
            print("\nEnter your question (or 'quit' to exit):")
            query = input("> ")
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
                
            print("\nAnalyzing...")
            response = agent.get_insights(query)
            print("\nInsights:", response)
            
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please update your .env file with the correct database credentials.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()