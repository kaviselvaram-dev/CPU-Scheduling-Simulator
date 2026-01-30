let processes = [];

const algoSelect = document.getElementById("algorithm");
const quantumField = document.getElementById("quantumField");
const priorityField = document.getElementById("priority");

algoSelect.addEventListener("change", () => {
  const algo = algoSelect.value;
  // Show quantum only for Round Robin
  quantumField.style.display = algo === "Round Robin" ? "block" : "none";
  // Show priority for both Priority algorithms
  priorityField.style.display = algo.includes("Priority") ? "inline-block" : "none";
});

document.getElementById("addBtn").addEventListener("click", () => {
  const name = document.getElementById("pname").value;
  const arrival = document.getElementById("arrival").value;
  const burst = document.getElementById("burst").value;
  const priority = document.getElementById("priority").value || "";

  if (!name || arrival === "" || burst === "") {
    alert("Please fill all required fields!");
    return;
  }

  const algo = algoSelect.value;
  if (algo.includes("Priority")) {
    processes.push(`${name},${arrival},${burst},${priority}`);
  } else {
    processes.push(`${name},${arrival},${burst},`);
  }

  alert(`Process ${name} added successfully!`);
});

document.getElementById("runBtn").addEventListener("click", () => {
  const form = document.getElementById("runForm");
  document.getElementById("algoInput").value = algoSelect.value;
  document.getElementById("quantumInput").value = document.getElementById("quantum").value;

  const container = document.getElementById("processInputs");
  container.innerHTML = "";
  processes.forEach(p => {
    const input = document.createElement("input");
    input.type = "hidden";
    input.name = "process";
    input.value = p;
    container.appendChild(input);
  });

  if (processes.length === 0) {
    alert("Add at least one process!");
    return;
  }

  form.submit();
});
