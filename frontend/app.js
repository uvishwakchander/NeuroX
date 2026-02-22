// -------------------------
// QUEST CREATION (AI)
// -------------------------
async function addTask() {
  const task = document.getElementById("taskInput").value;
  if (!task) return;

  const res = await fetch("http://localhost:8000/quest", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ task })
  });

  const data = await res.json();

  const div = document.createElement("div");
  div.innerHTML = `${data.quest} <br>🌟 XP: +${data.xp}`;
  document.getElementById("taskList").appendChild(div);

  document.getElementById("taskInput").value = "";
}

// -------------------------
// COMMUNICATION COPILOT
// -------------------------
async function clarify() {
  const text = document.getElementById("rawMessage").value;

  const res = await fetch("http://localhost:8000/clarify", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ text })
  });

  const data = await res.json();
  document.getElementById("clarifiedMessage").innerText = data.clarified;
}

// -------------------------
// BURNOUT CHECK
// -------------------------
async function checkBurnout() {
  const res = await fetch("http://localhost:8000/burnout", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      hours_worked: 9,
      tasks_done: 3,
      breaks_taken: 1
    })
  });

  const data = await res.json();
  document.getElementById("burnoutStatus").innerText =
    data.status + " " + data.suggestion;
}
