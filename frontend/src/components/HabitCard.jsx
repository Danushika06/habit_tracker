import { API_URL } from '../config'
import { getToday } from '../utils/date'

function HabitCard({ habit, onHabitChanged }) {
  const today = getToday()
  const isCheckedToday = habit.logs.some((log) => log.completed_date === today)

  const handleToggle = () => {
    fetch(`${API_URL}/habits/${habit.id}/toggle/`, {
      method: 'POST',
    }).then(() => onHabitChanged())
  }

  const handleDelete = () => {
    fetch(`${API_URL}/habits/${habit.id}/`, {
      method: 'DELETE',
    }).then(() => onHabitChanged())
  }

  return (
    <div className="rounded-lg border border-gray-300 p-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold">{habit.name}</h2>
          <p className="text-sm text-gray-500">{habit.category}</p>
        </div>
        <div className="flex items-center gap-3">
          <input
            type="checkbox"
            checked={isCheckedToday}
            onChange={handleToggle}
            className="h-5 w-5"
          />
          <button onClick={handleDelete} className="text-sm text-red-500">
            Delete
          </button>
        </div>
      </div>
    </div>
  )
}

export default HabitCard
