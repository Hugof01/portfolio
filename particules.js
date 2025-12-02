// Tableau pour stocker les instances
var particulesSystemInstances = [];

window.onload = function () {
    var particulesCounter = 0;
    var allItem = document.getElementsByClassName('particules');

    for (var i = 0; i < allItem.length; ++i) {
        particulesSystemInstances[particulesCounter] = new ParticulesSystem(allItem[i]);
        particulesSystemInstances[particulesCounter].init();
        particulesCounter++;
    }
};

// Constructeur (renommé avec majuscule pour convention)
var ParticulesSystem = function (dom) {

    /*=========================================\
        CONSTRUCTEUR
    \=========================================*/

    var self         = this,
        data         = dom.dataset,
        labels       = data.labels ? data.labels.split(',') : false,
        initialLines = data.colorLines || 'rgba(145,249,240,0.5)',
        initialDots  = data.colorDots  || 'rgba(145,249,240,0.5)',
        colorLabels  = data.colorLabels || 'rgba(145,249,240,0.5)',
        mouse        = {x: 10, y: 10},
        canvas       = document.createElement("canvas"),
        canvasDom,
        ctx          = canvas.getContext("2d"),
        retina       = window.devicePixelRatio > 1,
        particles    = [],
        patriclesNum = 1000,
        rad          = 5;

    if (retina) {
        patriclesNum *= 2;
        rad++;
    }

    /* === Couleurs dynamiques accessibles de l'extérieur === */
    self.colorDots  = initialDots;
    self.colorLines = initialLines;

    /*=========================================\
        INIT
    \=========================================*/

    self.init = function () {
        dom.appendChild(canvas);
        canvasDom = dom.querySelector('canvas');

        self.setCanvasSize(canvasDom);
        window.addEventListener("resize", self.setCanvasSize);

        for (var i = 0; i < patriclesNum; i++) {
            particles.push(new multi_part());
        }

        canvasDom.addEventListener('mousemove', self.mouseMoveCanvas, false);

        window.setInterval(function () {
            self.move_part()
        }, 33);
    };

    /*=========================================\
        PARTICULE
    \=========================================*/

    function multi_part() {
        this.x   = Math.random() * canvasDom.width;
        this.y   = Math.random() * canvasDom.height;
        this.vx  = Math.random() * 0.88 - 0.44;
        this.vy  = Math.random() * 0.88 - 0.44;
        this.rad = Math.random() * 2 + 1;
    }
    

    /*=========================================\
        METHODS
    \=========================================*/

    self.setCanvasSize = function () {
        if (retina) {
            canvasDom.width  = canvasDom.parentNode.offsetWidth * 2;
            canvasDom.height = canvasDom.parentNode.offsetHeight * 2;
        } else {
            canvasDom.width  = canvasDom.parentNode.offsetWidth;
            canvasDom.height = canvasDom.parentNode.offsetHeight;
        }
        canvasDom.style.width  = canvasDom.parentNode.offsetWidth + "px";
        canvasDom.style.height = canvasDom.parentNode.offsetHeight + "px";
    };

    self.move_part = function () {
        ctx.clearRect(0, 0, canvasDom.width, canvasDom.height);

        for (var i = 0; i < patriclesNum; i++) {
            var temp = particles[i];
            var distParticule = self.findDistance(temp, mouse);

            /* === LIENS PARTICULE <-> SOURIS === */
            var distretina = retina ? 150 : 100;
            if (distParticule < distretina) {
                self.createLine(temp, mouse, distParticule);
            }

            /* === LIENS ENTRE PARTICULES === */
            for (var j = 0; j < patriclesNum; j++) {
                var temp2 = particles[j];
                if (temp !== temp2) {
                    var d = self.findDistance(temp, temp2);
                    if (d < distretina) {
                        self.createLine(temp, temp2, d);
                    }
                }
            }

            /* === POINTS === */
            ctx.fillStyle = self.colorDots;
            ctx.globalAlpha = 1;
            ctx.beginPath();
            ctx.arc(temp.x, temp.y, temp.rad, 0, Math.PI * 2, true);
            ctx.fill();
            ctx.closePath();

            /* === MOUVEMENT === */
            temp.x += temp.vx;
            temp.y += temp.vy;

            if (temp.x > canvasDom.width) temp.x = 0;
            if (temp.x < 0) temp.x = canvasDom.width;
            if (temp.y > canvasDom.height) temp.y = 0;
            if (temp.y < 0) temp.y = canvasDom.height;
        }
    };

    self.createLine = function (p1, p2, d) {
        ctx.strokeStyle = self.colorLines;
        ctx.lineWidth = 0.8;                 // Lignes fines
        ctx.globalAlpha = 12 / d - 0.08;      // Opacité réduite
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();
    };

    self.findDistance = function (p1, p2) {
        return Math.sqrt(
            Math.pow(p2.x - p1.x, 2) +
            Math.pow(p2.y - p1.y, 2)
        );
    };

    self.mouseMoveCanvas = function (event) {
        var rect = canvasDom.getBoundingClientRect();
        mouse = {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top
        };
    };
};