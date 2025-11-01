// Canvases
var canvas  = document.getElementById('canvas'),
    ctx     = canvas.getContext('2d'),
    canvas2 = document.getElementById('canvas2'),
    ctx2    = canvas2.getContext('2d');

// Dimensions
var cw = window.innerWidth,
    ch = window.innerHeight;

canvas.width = canvas2.width = cw;
canvas.height = canvas2.height = ch;

// Paramètres Matrix (version soft)
var charArr = 'abcdefghijklmnopqrstuvwxyz0123456789'.split('');
var fallingCharArr = [];
var fontSize = 14; // un peu plus grand => plus doux
var maxColumns = Math.floor(cw / fontSize);

// Utils
function randomInt(min, max){ return Math.floor(Math.random()*(max-min)+min); }
function randomFloat(min, max){ return Math.random()*(max-min)+min; }

// Point "caractère"
function Point(x, y){
  this.x = x;
  this.y = y;
  this.speed = randomFloat(1, 2); // vitesse douce
}
Point.prototype.draw = function(){
  this.value = charArr[randomInt(0, charArr.length)].toUpperCase();

  // halo pâle
  ctx2.fillStyle = 'rgba(255,255,255,0.5)';
  ctx2.font = fontSize + 'px sans-serif';        // <- CORRECTION ici
  ctx2.fillText(this.value, this.x, this.y);

  // caractère vert
  ctx.fillStyle = '#0F0';
  ctx.font = fontSize + 'px sans-serif';         // <- CORRECTION ici
  ctx.fillText(this.value, this.x, this.y);

  this.y += this.speed;
  if (this.y > ch){
    this.y = randomFloat(-100, 0);
    this.speed = randomFloat(1.5, 3);
  }
};

// Initialisation colonnes
function initColumns(){
  fallingCharArr = [];
  maxColumns = Math.floor(cw / fontSize);
  for (var i = 0; i < maxColumns; i++){
    fallingCharArr.push(new Point(i * fontSize, randomFloat(-500, 0)));
  }
}
initColumns();

// Animation
function update(){
  // traînée (rémanence) — plus la valeur est grande, plus c'est "fumé"
  ctx.fillStyle = 'rgba(0,0,0,0.08)';
  ctx.fillRect(0, 0, cw, ch);

  // couche halo nettoyée à chaque frame
  ctx2.clearRect(0, 0, cw, ch);

  for (var i = 0; i < fallingCharArr.length; i++){
    fallingCharArr[i].draw();
  }
  requestAnimationFrame(update);
}
update();

// Resize responsable
window.addEventListener('resize', function(){
  cw = window.innerWidth;
  ch = window.innerHeight;
  canvas.width = canvas2.width = cw;
  canvas.height = canvas2.height = ch;
  initColumns();
});
