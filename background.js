// Effet Matrix bleuté feutré pour le portfolio Hugo FRANÇOIS
window.addEventListener("load", function () {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const canvas2 = document.getElementById("canvas2");
    const ctx2 = canvas2.getContext("2d");
  
    let cw = window.innerWidth;
    let ch = window.innerHeight;
  
    canvas.width = canvas2.width = cw;
    canvas.height = canvas2.height = ch;
  
    // Jeu de caractères "cyber"
    const charArr = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@&$%".split("");
    const fallingCharArr = [];
    const fontSize = 14;
    let maxColumns = Math.floor(cw / fontSize);
  
    function randomInt(min, max) {
      return Math.floor(Math.random() * (max - min) + min);
    }
    function randomFloat(min, max) {
      return Math.random() * (max - min) + min;
    }
  
    // Objet caractère
    function Point(x, y) {
      this.x = x;
      this.y = y;
      this.speed = randomFloat(1, 2.2);
      this.value = charArr[randomInt(0, charArr.length)];
    }
  
    Point.prototype.draw = function () {
      this.value = charArr[randomInt(0, charArr.length)];
  
      // Halo clair
      ctx2.fillStyle = "rgba(255,255,255,0.4)";
      ctx2.font = fontSize + "px monospace";
      ctx2.fillText(this.value, this.x, this.y);
  
      // Couleur principale (bleu accentué)
      ctx.fillStyle = "#66fcf1";
      ctx.font = fontSize + "px monospace";
      ctx.fillText(this.value, this.x, this.y);
  
      this.y += this.speed;
      if (this.y > ch) {
        this.y = randomFloat(-100, 0);
        this.speed = randomFloat(1, 2.2);
      }
    };
  
    // Init des colonnes
    function initColumns() {
      fallingCharArr.length = 0;
      maxColumns = Math.floor(cw / fontSize);
      for (let i = 0; i < maxColumns; i++) {
        fallingCharArr.push(new Point(i * fontSize, randomFloat(-1000, 0)));
      }
    }
    initColumns();
  
    // Animation
    function update() {
      // arrière-plan sombre semi-transparent pour effet "traînée"
      ctx.fillStyle = "rgba(0,0,0,0.08)";
      ctx.fillRect(0, 0, cw, ch);
  
      ctx2.clearRect(0, 0, cw, ch);
  
      for (let i = 0; i < fallingCharArr.length; i++) {
        fallingCharArr[i].draw();
      }
  
      requestAnimationFrame(update);
    }
    update();
  
    // Adaptation sur redimensionnement
    window.addEventListener("resize", () => {
      cw = window.innerWidth;
      ch = window.innerHeight;
      canvas.width = canvas2.width = cw;
      canvas.height = canvas2.height = ch;
      initColumns();
    });
  });
  