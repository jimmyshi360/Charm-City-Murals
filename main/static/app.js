
particlesJS("particles-js2", {
	"particles": {
						"number": {
							"value": 80,
							"density": {
								"enable": true
							},

						},
						"color": {
							"value": ["#fff"]
						},
						"opacity": {
							"value": 0.6,
							"random": false,
								"anim": {
									"enable": true,
									"speed": 1,
									"opacity_min": 0.4,
									"sync": false
								}
						},
						"shape": {
							"type": "circle"
						},
						"size": {
							"value": 1,
							"random": true
						},
						"line_linked": {
							"enable": true
						},
						"move": {
							"enable": true,
							"speed": 1,
							"random": true,
							"direction": "none",
							"straight": false
						}
				},
				"interactivity": {
						"detect_on": "canvas",
						"events": {
								"onhover": {
									"enable": true
								}
							},
					"modes": {
						"push": {
							"particles_nb": 3
						}
				}
		}
});

particlesJS("particles-js", {
  "particles": {
    "number": {
      "value": 355,
      "density": {
        "enable": true,
        "value_area": 789.1476416322727
      }
    },
    "color": {
      "value": "#ffa500"
    },
    "shape": {
      "type": "polygon",
      "stroke": {
        "width": 0,
        "color": "#ffa500"
      },
      "polygon": {
        "nb_sides": 4
      },
      "image": {
        "src": "img/github.svg",
        "width": 100,
        "height": 150
      }
    },
    "opacity": {
      "value": 1,
      "random": false,
      "anim": {
        "enable": true,
        "speed": 1,
        "opacity_min": 0.8,
        "sync": false
      }
    },
    "size": {
      "value": 1.5,
      "random": true,
      "anim": {
        "enable": true,
        "speed": 2,
        "size_min": 0,
        "sync": false
      }
    },
    "line_linked": {
      "enable": false,
      "distance": 150,
      "color": "#ffffff",
      "opacity": 0.4,
      "width": 1
    },
    "move": {
      "enable": true,
      "speed": 2,
      "direction": "top",
      "random": false,
      "straight": true,
      "out_mode": "out",
      "bounce": false,
      "attract": {
        "enable": false,
        "rotateX": 0,
        "rotateY": 0
      }
    }
  },
  "interactivity": {
      "detect_on": "canvas",
      "events": {
        "onhover": {
          "enable": true,
          "mode": "repulse"
        },
        "onclick": {
          "enable": true,
          "mode": "push"
        },
        "resize": true
      },
      "modes": {
        "grab": {
          "distance": 200,
          "line_linked": {
            "opacity": 1
          }
        },
        "bubble": {
          "distance": 200,
          "size": 40,
          "duration": 2,
          "opacity": 8,
          "speed": 3
        },
        "repulse": {
          "distance": 100
        },
        "push": {
          "particles_nb": 4
        },
        "remove": {
          "particles_nb": 2
        }
      }
    },
  "retina_detect": true
});