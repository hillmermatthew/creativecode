//"Planets" by Matthew Hillmer
// It's like a screensaver or something
// 10/13/19

// Note: If you edit the size of the window, you may need to adjust the quantity, speed, and scale of the planets using the parameters below.  Or you can change them just for fun, that's cool too.

var numPlanets = 100; //edit this to change number of planets
var speed = 0.02;  //edit this to change the speed
var pScale = 1.5;  //edit this to change the size of planets


var planets = [];

function setup() {
  createCanvas(1920, 1080, WEBGL);
  background(0,0,0);
  for (var i = 0; i < numPlanets; i++) {
    planets[i] = new planet(speed,pScale);
  }
}

function draw() {
  background(0,0,0);
  
  for(var i=0; i<planets.length; i++)
  {
    planets[i].update();
  }
}

function planet(speed,scale)
{
  this.Dspeed = speed;
  this.z = random(-1900,-200);
  this.x = random(-width,width);
  this.rot = 0;
  this.y = -5.0;
  this.delay = random(0,(500));
  this.size = random([5,5,10,10,30,30,60,100,300]) * scale;
  this.randomColor = color(random(255),random(255),random(255));
  
  this.update = function()
  {
    if(this.delay > 0)
    {
      this.delay--;
    }
    else
    {
      this.rot = this.rot + 0.01;
      this.y += this.Dspeed;
      noFill();
      stroke(this.randomColor);
      push();
      translate(this.x, height * this.y, this.z);
      rotateY(this.rot);
      sphere(this.size);
      pop();
    
      if(this.rot>355)
      {
        this.rot=0;
      }
      
      if(this.y > 4)
      {
        this.y = -5.0;
        this.z = random(-1900,200);
        this.x = random(-width,width);
        
        this.delay = random(0,100);
        this.size = random([5,5,10,10,30,30,60,100,300]) * scale;
      }
    }
  }   
}
