const TaskList = ({ tasks, onEdit, onDelete, onStatusChange }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'TODO':
        return 'bg-blue-100 text-blue-800';
      case 'DOING':
        return 'bg-yellow-100 text-yellow-800';
      case 'DONE':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'HIGH':
        return 'text-red-600';
      case 'MEDIUM':
        return 'text-yellow-600';
      case 'LOW':
        return 'text-green-600';
      default:
        return 'text-gray-600';
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
        No tasks found. Create your first task!
      </div>
    );
  }

  return (
    <div className="grid gap-4">
      {tasks.map((task) => (
        <div key={task.id} className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
          <div className="flex justify-between items-start mb-3">
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900">{task.title}</h3>
              {task.description && (
                <p className="text-gray-600 mt-1">{task.description}</p>
              )}
            </div>
            <div className="flex gap-2 ml-4">
              <button
                onClick={() => onEdit(task)}
                className="text-blue-600 hover:text-blue-800"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="text-red-600 hover:text-red-800"
              >
                Delete
              </button>
            </div>
          </div>

          <div className="flex items-center gap-4 mt-4">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(task.status)}`}>
              {task.status}
            </span>
            <span className={`text-sm font-medium ${getPriorityColor(task.priority)}`}>
              {task.priority} Priority
            </span>
            {task.due_date && (
              <span className="text-sm text-gray-500">
                Due: {new Date(task.due_date).toLocaleDateString()}
              </span>
            )}
          </div>

          <div className="mt-4 flex gap-2">
            {task.status !== 'TODO' && (
              <button
                onClick={() => onStatusChange(task.id, 'TODO')}
                className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded hover:bg-blue-200"
              >
                Move to To Do
              </button>
            )}
            {task.status !== 'DOING' && (
              <button
                onClick={() => onStatusChange(task.id, 'DOING')}
                className="text-xs bg-yellow-100 text-yellow-700 px-3 py-1 rounded hover:bg-yellow-200"
              >
                Move to Doing
              </button>
            )}
            {task.status !== 'DONE' && (
              <button
                onClick={() => onStatusChange(task.id, 'DONE')}
                className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded hover:bg-green-200"
              >
                Mark as Done
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;
