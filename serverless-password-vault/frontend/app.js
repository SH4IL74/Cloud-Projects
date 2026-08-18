// LocalStack API Gateway endpoint
const API_BASE_URL = "http://localhost:4566/_aws/execute-api/b5g9kynfy7/prod";

const lengthSlider = document.getElementById("length");
const lengthVal = document.getElementById("length-val");
const vaultForm = document.getElementById("vault-form");
const resultBox = document.getElementById("result-box");
const generatedPwdInput = document.getElementById("generated-pwd");
const strengthBadge = document.getElementById("strength-badge");
const copyBtn = document.getElementById("copy-btn");
const recordsBody = document.getElementById("records-body");
const refreshBtn = document.getElementById("refresh-btn");

// Update length display on slider change
lengthSlider.addEventListener("input", (e) => {
  lengthVal.textContent = e.target.value;
});

// Copy to clipboard
copyBtn.addEventListener("click", () => {
  navigator.clipboard.writeText(generatedPwdInput.value);
  copyBtn.textContent = "✅";
  setTimeout(() => (copyBtn.textContent = "📋"), 1500);
});

// Fetch stored records from DynamoDB via API Gateway
async function fetchRecords() {
  try {
    const res = await fetch(`${API_BASE_URL}/passwords`);
    const data = await res.json();
    const records = data.records || [];

    if (records.length === 0) {
      recordsBody.innerHTML = `<tr><td colspan="4" class="loading-cell">No records found. Generate one!</td></tr>`;
      return;
    }

    records.sort((a, b) => (b.created_at || 0) - (a.created_at || 0));

    recordsBody.innerHTML = records
      .map((r) => {
        const dateStr = r.created_at
          ? new Date(r.created_at * 1000).toLocaleString()
          : "N/A";
        const strengthClass =
          r.strength === "STRONG"
            ? "badge-strong"
            : r.strength === "MEDIUM"
            ? "badge-medium"
            : "badge-weak";
        return `
          <tr>
            <td><strong>${r.label || "Unnamed"}</strong></td>
            <td>${r.length || "-"}</td>
            <td><span class="badge ${strengthClass}">${r.strength || "N/A"}</span></td>
            <td>${dateStr}</td>
          </tr>
        `;
      })
      .join("");
  } catch (err) {
    recordsBody.innerHTML = `<tr><td colspan="4" class="loading-cell" style="color: var(--weak);">Failed to load records from API.</td></tr>`;
  }
}

// Generate new password
vaultForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    label: document.getElementById("label").value,
    length: parseInt(lengthSlider.value),
    use_uppercase: document.getElementById("use_uppercase").checked,
    use_digits: document.getElementById("use_digits").checked,
    use_symbols: document.getElementById("use_symbols").checked,
  };

  try {
    const res = await fetch(`${API_BASE_URL}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (res.ok) {
      generatedPwdInput.value = data.generated_password;
      strengthBadge.textContent = data.strength;
      strengthBadge.className = `badge badge-${data.strength.toLowerCase()}`;
      resultBox.classList.remove("hidden");

      // Refresh table
      fetchRecords();
    } else {
      alert("Error generating password: " + (data.message || "Unknown error"));
    }
  } catch (err) {
    alert("API Request Failed: " + err.message);
  }
});

refreshBtn.addEventListener("click", fetchRecords);

// Initial load
fetchRecords();