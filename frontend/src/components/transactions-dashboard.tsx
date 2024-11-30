"use client"

import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

import { useEffect, useState } from 'react'


import axios from 'axios'
import { UUID } from 'crypto'

// Sample data
const transactions = [
  { id: 1, category: 'Food', amount: 50, date: '2023-05-01' },
  { id: 2, category: 'Transport', amount: 30, date: '2023-05-02' },
  { id: 3, category: 'Entertainment', amount: 100, date: '2023-05-03' },
  { id: 4, category: 'Food', amount: 75, date: '2023-05-04' },
  { id: 5, category: 'Transport', amount: 25, date: '2023-05-05' },
]

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

type Transactions = {
  id: UUID,
  category: String,
  amount: Number,
  remarks: String,
  transaction_date: String,
}

type PieData = {
  name: string,
  value: Number
}
export default function TransactionsDashboard() {

  const [allTxns, setAllTxns] = useState<Transactions[]>([])
  const [pieData, setPieData] = useState<PieData[]>([])

  const fetchPieData = async () => {
    try {
      const response = await axios.get("http://localhost:8000/transactions/category")
      setPieData(response.data)
    } catch (e: any) {
      console.error(e)
    }
  }

  const fetchAllTransaction = async () => {
    try {
      const response = await axios.get("http://localhost:8000/transactions")
      setAllTxns(response.data)
    } catch (e: any) {
      console.error(e)
    }
  }

  useEffect(() => {
    fetchAllTransaction()
    fetchPieData()
  }, [])


  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Transaction Distribution</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {pieData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Recent Transactions</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Category</TableHead>
                <TableHead>Amount</TableHead>
                <TableHead>Date</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {allTxns.map((transaction) => (
                <TableRow key={transaction.id}>
                  <TableCell>{transaction.category}</TableCell>
                  <TableCell>${transaction.amount.toString()}</TableCell>
                  <TableCell>{transaction.transaction_date}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}


