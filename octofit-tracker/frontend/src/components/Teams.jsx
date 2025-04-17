import { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    fetch('https://bookish-acorn-rp7g575477vf5vj-8000.app.github.dev/api/teams/')
      .then(response => response.json())
      .then(data => setTeams(data))
      .catch(error => console.error('Error fetching teams:', error));
  }, []);

  return (
    <div>
      <h1>Teams</h1>
      <div className="table-responsive">
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Team Name</th>
              <th>Members</th>
            </tr>
          </thead>
          <tbody>
            {teams.map(team => {
              console.log(team);
              return (
                <tr key={team._id}>
                  <td>{team.name}</td>
                  <td>{JSON.parse(team.members.replace(/'/g, '"')).join()}</td>
                </tr>
              );
            }
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Teams;