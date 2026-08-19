import { useState, useEffect } from 'react'
import HabitCard from './components/HabitCard'
import { API_URL } from './config'

function App() {
  const [habits, setHabits] = useState([])
  const [name, setName] = useState('')
  const [category, setCategory] = useState('')

  const fetchHabits = () => {
    fetch(`${API_URL}/habits/`)
      .then((response) => response.json())
      .then((data) => setHabits(data))
  }

  useEffect(() => {
    fetchHabits()
  }, [])

  const handleAddHabit = (event) => {
    event.preventDefault()
    fetch(`${API_URL}/habits/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, category }),
    }).then(() => {
      setName('')
      setCategory('')
      fetchHabits()
    })
  }

  return (
    <div className="mx-auto max-w-2xl p-6">
      <h1 className="mb-4 text-2xl font-bold">Habit Tracker</h1>

      <form onSubmit={handleAddHabit} className="mb-6 flex gap-2">
        <input
          type="text"
          placeholder="Habit name"
          value={name}
          onChange={(event) => setName(event.target.value)}
          className="flex-1 rounded border border-gray-300 px-3 py-2"
          required
        />
        <input
          type="text"
          placeholder="Category"
          value={category}
          onChange={(event) => setCategory(event.target.value)}
          className="flex-1 rounded border border-gray-300 px-3 py-2"
          required
        />
        <button type="submit" className="rounded bg-blue-600 px-4 py-2 text-white">
          Add
        </button>
      </form>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        {habits.map((habit) => (
          <HabitCard key={habit.id} habit={habit} onHabitChanged={fetchHabits} />
        ))}
      </div>
    </div>
  )
}

export default App
