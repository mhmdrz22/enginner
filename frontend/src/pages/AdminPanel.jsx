import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from '../api/axios';

const AdminPanel = () => {
  const [users, setUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [subject, setSubject] = useState('Notification from TaskBoard');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [notification, setNotification] = useState(null);
  
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is admin - silent redirect without alert
    if (!user?.is_staff && !user?.is_superuser) {
      setNotification({ 
        type: 'error', 
        message: 'Access denied. Admin privileges required.' 
      });
      // Redirect after showing notification
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
      return;
    }
    
    fetchOverview();
  }, [user, navigate]);

  const fetchOverview = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/accounts/admin/overview/');
      setUsers(response.data.users);
    } catch (error) {
      console.error('Error fetching overview:', error);
      setNotification({ type: 'error', message: 'Failed to load users data' });
    } finally {
      setLoading(false);
    }
  };

  const handleUserSelect = (userId) => {
    setSelectedUsers(prev => {
      if (prev.includes(userId)) {
        return prev.filter(id => id !== userId);
      } else {
        return [...prev, userId];
      }
    });
  };

  const handleSelectAll = () => {
    if (selectedUsers.length === users.length) {
      setSelectedUsers([]);
    } else {
      setSelectedUsers(users.map(u => u.id));
    }
  };

  const handleSendEmail = async () => {
    if (selectedUsers.length === 0) {
      setNotification({ type: 'error', message: 'Please select at least one user' });
      return;
    }

    if (!message.trim()) {
      setNotification({ type: 'error', message: 'Please enter a message' });
      return;
    }

    setSending(true);
    setNotification(null);

    try {
      const selectedEmails = users
        .filter(u => selectedUsers.includes(u.id))
        .map(u => u.email);

      const response = await axios.post('/accounts/admin/notify/', {
        recipients: selectedEmails,
        subject: subject,
        message: message
      });

      setNotification({
        type: 'success',
        message: `Email queued successfully! Job ID: ${response.data.job_id}`
      });
      
      // Reset form
      setSelectedUsers([]);
      setMessage('');
    } catch (error) {
      setNotification({
        type: 'error',
        message: error.response?.data?.error || 'Failed to send email'
      });
    } finally {
      setSending(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Admin Panel</h1>
            <p className="text-sm text-gray-600">Manage users and send notifications</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => navigate('/dashboard')}
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
            >
              Dashboard
            </button>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {/* Notification */}
        {notification && (
          <div className={`mb-4 p-4 rounded-lg flex items-start gap-3 ${
            notification.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            {notification.type === 'success' ? (
              <svg className="w-6 h-6 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            ) : (
              <svg className="w-6 h-6 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            )}
            <div className="flex-1">
              {notification.message}
            </div>
            <button
              onClick={() => setNotification(null)}
              className="text-gray-500 hover:text-gray-700"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Users Table */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Users Overview</h2>
              <button
                onClick={handleSelectAll}
                className="text-sm text-blue-600 hover:underline"
              >
                {selectedUsers.length === users.length ? 'Deselect All' : 'Select All'}
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Select
                    </th>
                    <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Email
                    </th>
                    <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Username
                    </th>
                    <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Open Tasks
                    </th>
                    <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Total Tasks
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {users.map((user) => (
                    <tr key={user.id} className="hover:bg-gray-50">
                      <td className="px-3 py-4">
                        <input
                          type="checkbox"
                          checked={selectedUsers.includes(user.id)}
                          onChange={() => handleUserSelect(user.id)}
                          className="w-4 h-4 text-blue-600 rounded"
                        />
                      </td>
                      <td className="px-3 py-4 text-sm text-gray-900">
                        {user.email}
                      </td>
                      <td className="px-3 py-4 text-sm text-gray-900">
                        {user.username}
                      </td>
                      <td className="px-3 py-4 text-sm">
                        <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded">
                          {user.open_tasks}
                        </span>
                      </td>
                      <td className="px-3 py-4 text-sm text-gray-900">
                        {user.total_tasks}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Email Form */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Send Email Notification</h2>
            
            <div className="mb-4">
              <div className="text-sm text-gray-600 mb-2">
                Selected: {selectedUsers.length} user(s)
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Subject
              </label>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="Email subject"
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Message (Markdown supported)
              </label>
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                rows="10"
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500 font-mono text-sm"
                placeholder="Enter your message here...\n\nYou can use Markdown:\n# Heading\n**bold** *italic*\n- List item"
              />
            </div>

            <button
              onClick={handleSendEmail}
              disabled={sending || selectedUsers.length === 0}
              className="w-full bg-green-500 text-white py-3 rounded-lg hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {sending ? 'Sending...' : `Send Email to ${selectedUsers.length} User(s)`}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AdminPanel;
