```javascript
// ========================================
// NEON SYSTEM
// JavaScript
// ========================================


// ================================
// DIGITAL CLOCK
// ================================

function updateClock() {
    const clock = document.getElementById("clock");
    const date = document.getElementById("date");

    if (!clock || !date) {
        return;
    }

    const now = new Date();

    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const seconds = String(now.getSeconds()).padStart(2, "0");

    clock.textContent = hours + ":" + minutes + ":" + seconds;

    const days = [
        "Minggu",
        "Senin",
        "Selasa",
        "Rabu",
        "Kamis",
        "Jumat",
        "Sabtu"
    ];

    const months = [
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember"
    ];

    date.textContent =
        days[now.getDay()] +
        ", " +
        now.getDate() +
        " " +
        months[now.getMonth()] +
        " " +
        now.getFullYear();
}

updateClock();

setInterval(updateClock, 1000);


// ================================
// SYSTEM POWER
// ================================

let powerValue = 87;

const powerText = document.getElementById("power");
const powerBar = document.getElementById("powerBar");

function updatePower() {

    if (!powerText || !powerBar) {
        return;
    }

    const change = Math.floor(Math.random() * 5) - 2;

    powerValue = powerValue + change;

    if (powerValue > 99) {
        powerValue = 99;
    }

    if (powerValue < 70) {
        powerValue = 70;
    }

    powerText.textContent = powerValue + "%";

    powerBar.style.width = powerValue + "%";
}

setInterval(updatePower, 3000);


// ================================
// INITIALIZE BUTTON
// ================================

const startButton = document.getElementById("startButton");
const terminal = document.getElementById("terminal");

if (startButton && terminal) {

    startButton.addEventListener("click", function () {

        startButton.disabled = true;

        startButton.innerHTML =
            "<span>SYSTEM INITIALIZING...</span>";

        const messages = [
            "Scanning environment...",
            "Checking security...",
            "Establishing secure connection...",
            "Loading neural interface...",
            "Power synchronization complete.",
            "Initialization successful."
        ];

        let index = 0;

        const interval = setInterval(function () {

            const line = document.createElement("p");

            line.innerHTML =
                '<span class="green">[SYSTEM]</span> ' +
                messages[index];

            terminal.appendChild(line);

            index++;

            if (index >= messages.length) {

                clearInterval(interval);

                startButton.innerHTML =
                    "<span>SYSTEM ONLINE ✓</span>";

                startButton.disabled = false;
            }

        }, 700);
    });
}


// ================================
// PARTICLE BACKGROUND
// ================================

const canvas = document.getElementById("particles");

if (canvas) {

    const ctx = canvas.getContext("2d");

    let particles = [];

    const mouse = {
        x: null,
        y: null,
        radius: 120
    };


    // Resize canvas

    function resizeCanvas() {

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        createParticles();
    }


    window.addEventListener("resize", resizeCanvas);


    // Mouse position

    window.addEventListener("mousemove", function (event) {

        mouse.x = event.clientX;
        mouse.y = event.clientY;

    });


    window.addEventListener("mouseleave", function () {

        mouse.x = null;
        mouse.y = null;

    });


    // Create particles

    function createParticles() {

        particles = [];

        const amount = Math.min(
            Math.floor(
                (canvas.width * canvas.height) / 12000
            ),
            150
        );


        for (let i = 0; i < amount; i++) {

            particles.push({

                x: Math.random() * canvas.width,

                y: Math.random() * canvas.height,

                size: Math.random() * 2 + 0.5,

                speedX:
                    (Math.random() - 0.5) * 0.4,

                speedY:
                    (Math.random() - 0.5) * 0.4
            });
        }
    }


    // Draw particles

    function drawParticles() {

        ctx.clearRect(
            0,
            0,
            canvas.width,
            canvas.height
        );


        for (let i = 0; i < particles.length; i++) {

            const particle = particles[i];


            particle.x =
                particle.x + particle.speedX;

            particle.y =
                particle.y + particle.speedY;


            // Loop screen

            if (particle.x < 0) {
                particle.x = canvas.width;
            }

            if (particle.x > canvas.width) {
                particle.x = 0;
            }

            if (particle.y < 0) {
                particle.y = canvas.height;
            }

            if (particle.y > canvas.height) {
                particle.y = 0;
            }


            // Mouse interaction

            if (mouse.x !== null && mouse.y !== null) {

                const dx =
                    particle.x - mouse.x;

                const dy =
                    particle.y - mouse.y;

                const distance =
                    Math.sqrt(
                        dx * dx + dy * dy
                    );


                if (distance < mouse.radius && distance > 0) {

                    const force =
                        (mouse.radius - distance)
                        / mouse.radius;


                    particle.x =
                        particle.x +
                        (dx / distance) *
                        force *
                        1.5;


                    particle.y =
                        particle.y +
                        (dy / distance) *
                        force *
                        1.5;
                }
            }


            // Draw particle

            ctx.beginPath();

            ctx.arc(
                particle.x,
                particle.y,
                particle.size,
                0,
                Math.PI * 2
            );

            ctx.fillStyle =
                "rgba(0, 247, 255, 0.7)";

            ctx.fill();


            // Connect particles

            for (
                let j = i + 1;
                j < particles.length;
                j++
            ) {

                const other =
                    particles[j];


                const dx =
                    particle.x - other.x;

                const dy =
                    particle.y - other.y;

                const distance =
                    Math.sqrt(
                        dx * dx + dy * dy
                    );


                if (distance < 100) {

                    ctx.beginPath();

                    ctx.moveTo(
                        particle.x,
                        particle.y
                    );

                    ctx.lineTo(
                        other.x,
                        other.y
                    );

                    ctx.strokeStyle =
                        "rgba(0, 247, 255, 0.08)";

                    ctx.lineWidth = 0.5;

                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(drawParticles);
    }


    resizeCanvas();

    drawParticles();
}


// ================================
// 3D CARD EFFECT
// ================================

const cards = document.querySelectorAll(".card");

cards.forEach(function (card) {

    card.addEventListener("mousemove", function (event) {

        const rect =
            card.getBoundingClientRect();

        const x =
            event.clientX - rect.left;

        const y =
            event.clientY - rect.top;

        const centerX =
            rect.width / 2;

        const centerY =
            rect.height / 2;

        const rotateX =
            ((y - centerY) / centerY) * -4;

        const rotateY =
            ((x - centerX) / centerX) * 4;

        card.style.transform =
            "perspective(600px) " +
            "rotateX(" + rotateX + "deg) " +
            "rotateY(" + rotateY + "deg) " +
            "translateY(-5px)";
    });


    card.addEventListener("mouseleave", function () {

        card.style.transform = "";

    });

});
```
