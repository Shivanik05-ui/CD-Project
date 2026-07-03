async function runParser() {

    const expr = document.getElementById("expr").value;

    try {

        const response = await fetch("/parse", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ expr: expr })
        });

        const data = await response.json();

        console.log("SERVER RESPONSE:", data);

        if (data.error) {
            alert("Server Error: " + data.error);
            return;
        }

        /* ---------- Grammar ---------- */

        let grammarText = "";

        for (const nt in data.grammar) {

            grammarText += nt + " → ";

            grammarText += data.grammar[nt]
                .map(p => p.join(" "))
                .join(" | ");

            grammarText += "\n";
        }

        document.getElementById("grammar").innerText = grammarText;


        /* ---------- FIRST ---------- */

        let firstText = "";

        for (const nt in data.first) {

            firstText +=
                "FIRST(" + nt + ") = { " +
                data.first[nt].join(", ") +
                " }\n";
        }

        document.getElementById("first").innerText = firstText;


        /* ---------- FOLLOW ---------- */

        let followText = "";

        for (const nt in data.follow) {

            followText +=
                "FOLLOW(" + nt + ") = { " +
                data.follow[nt].join(", ") +
                " }\n";
        }

        document.getElementById("follow").innerText = followText;


        /* ---------- Parsing Table ---------- */

        let tableText = "";

        for (const nt in data.table) {

            for (const term in data.table[nt]) {

                const prod = data.table[nt][term].join(" ");

                tableText +=
                    "M[" + nt + ", " + term + "] = " +
                    nt + " → " + prod + "\n";
            }
        }

        document.getElementById("table").innerText = tableText;


        /* ---------- Parsing Steps ---------- */

        let stepsText = "";

        stepsText += "STACK\t\tINPUT\t\tACTION\n";
        stepsText += "---------------------------------------------\n";

        data.steps.forEach(step => {

            stepsText +=
                step.stack + "\t\t" +
                step.input + "\t\t" +
                step.action + "\n";
        });

        document.getElementById("steps").innerText = stepsText;


        /* ---------- Parse Tree ---------- */

        if (data.tree) {

            const img = document.getElementById("tree");

            img.src = data.tree + "?t=" + new Date().getTime();

            img.style.display = "block";
        }

    }

    catch (err) {

        console.error("Frontend error:", err);

        alert("Parser error. Check browser console.");
    }
}