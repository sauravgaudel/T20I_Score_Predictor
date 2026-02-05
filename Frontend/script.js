document.querySelector('#predictForm').addEventListener('submit', async function(e) {
    e.preventDefault(); 

    const data = {
        batting_team: document.querySelector('#battingTeam').value,
        bowling_team: document.querySelector('#bowlingTeam').value,
        current_score: Number(document.querySelector('#current_score').value),
        overs: Number(document.querySelector('#overs').value),
        wicket_fall: Number(document.querySelector('#wickets').value),
        last_five: Number(document.querySelector('#last_5_overs').value)
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();

        const resultDiv = document.querySelector('#result');    
        resultDiv.style.display = 'block';

        resultDiv.innerHTML = `
            <div style="text-align: center; font-size: 18px; font-weight: bold;">
                Predicted Score: ${result.Probability}
            </div>
        `;

    } catch (err) {
        console.error(err);
        document.querySelector('#result').innerHTML = `
            <div style="text-align: center; color: #ff4d4f; font-weight: bold; font-size: 18px;">
                Something Went Wrong!!!
            </div>
        `;
    }
});
