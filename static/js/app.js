// Load workouts on page load
document.addEventListener('DOMContentLoaded', function() {
    loadWorkouts();
    
    const form = document.getElementById('workoutForm');
    if (form) {
        form.addEventListener('submit', addWorkout);
    }
});

async function loadWorkouts() {
    try {
        const response = await fetch('/api/workouts');
        const workouts = await response.json();
        displayWorkouts(workouts);
    } catch (error) {
        console.error('Error loading workouts:', error);
    }
}

function displayWorkouts(workouts) {
    const container = document.getElementById('workoutsList');
    if (!container) return;
    
    let html = '';
    for (const [category, sessions] of Object.entries(workouts)) {
        if (sessions.length > 0) {
            html += `<h3>${category}</h3><ul>`;
            sessions.slice(-5).forEach(entry => {
                html += `<li>${entry.exercise} - ${entry.duration} min</li>`;
            });
            html += '</ul>';
        }
    }
    container.innerHTML = html || '<p>No workouts logged yet.</p>';
}

async function addWorkout(e) {
    e.preventDefault();
    
    const formData = {
        category: document.getElementById('category').value,
        exercise: document.getElementById('exercise').value,
        duration: parseInt(document.getElementById('duration').value)
    };
    
    try {
        const response = await fetch('/api/workouts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            alert('Workout added successfully!');
            document.getElementById('workoutForm').reset();
            loadWorkouts();
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        console.error('Error adding workout:', error);
        alert('Error adding workout');
    }
}

