import React from 'react';
import { to_string, BACKEND_URL } from '../App'

class Baseline extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = { 
          seconds: -1,
          running: false,
          speed: 1000,
          sentence: [],
          full_sen: [],
          sen_options: [],
          isGenerating: false,
          hasChanged: false,
        };
        this.startClock = this.startClock.bind(this);
        this.triggerStart = this.triggerStart.bind(this);
        this.stopClock = this.stopClock.bind(this);
        this.redoGeneration = this.redoGeneration.bind(this);
        this.fasterGeneration = this.fasterGeneration.bind(this);
        this.slowerGeneration = this.slowerGeneration.bind(this);
        this.generation_started = this.generation_started.bind(this);
        this.generation_finished = this.generation_finished.bind(this);
        this.new_generation = this.new_generation.bind(this);
        this.generate_options = this.generate_options.bind(this);
        this.handle_typing = this.handle_typing.bind(this);
        this.option_choosed = this.option_choosed.bind(this);
        this.new_options = this.new_options.bind(this);
      }
    
      tick() {
        this.setState({
          seconds: this.state.seconds + 1,
        });
        if(this.state.seconds >= this.state.full_sen.length) {
          this.stopClock()
          this.setState({
            seconds: this.state.full_sen.length-1
          })
        }
        else {
          this.state.sentence.push(this.state.full_sen[this.state.seconds]);
          var ta = document.getElementById('field');
          ta.scrollLeft = ta.scrollWidth;
        }
      }
    
      triggerStart() {
        if(this.state.hasChanged || 
          (this.state.full_sen.length === this.state.sentence.length && this.state.sentence.length !== 0)) {
          this.new_generation(to_string(this.state.sentence))
        }
        else {
          this.startClock()
        }
      }
    
      startClock() {
        if(!this.state.running) {
          let intervalId = setInterval(() => this.tick(), this.state.speed);
          this.setState({
            interval: intervalId,
            running: true,
          });
        }
      }
    
      stopClock() {
        if(this.state.running) {
          clearInterval(this.state.interval);
          this.setState({
            running: false,
            hasChanged: false,
          })
        }
      }
    
      redoGeneration() {
        this.setState({
          seconds: -1,
          sentence: [],
        });
        if(!this.state.running) {
          this.startClock()
        }
      }
    
      componentWillUnmount() {
        clearInterval(this.state.interval);
      }
    
      fasterGeneration() {
        if(this.state.running) {
          clearInterval(this.state.interval);
          this.setState({speed: this.state.speed / 4})
          let intervalId = setInterval(() => this.tick(), this.state.speed);
          this.setState({
            interval: intervalId,
          })
        }
      }
    
      slowerGeneration() {
        if(this.state.running) {
          clearInterval(this.state.interval);
          this.setState({speed: this.state.speed * 4})
          let intervalId = setInterval(() => this.tick(), this.state.speed);
          this.setState({
            interval: intervalId,
          })
        }
      }
    
      generation_started(clearSentence) {
        this.stopClock()
        this.setState({
          seconds: -1,
          isGenerating: true,
        });
        if(clearSentence) {
          this.setState({
            sentence: [], 
          })
        }
      }
    
      generation_finished() {
        this.setState({
          isGenerating: false,
        });
        this.startClock()
      }
    
      new_generation(sentence) {
        this.generation_started(false)
        fetch(`${BACKEND_URL}/api/generate`, {
          method: 'POST',
          body: JSON.stringify({
              'content': sentence
          }),
          headers: {
              "Content-type": "aplication/json; charset=UTF-8"
            }
        }).then(response => response.json())
        .then(message => {
            this.setState({
              sentence: message.sentence.split(" "),
              full_sen: message.new_sentence,
              seconds : message.index - 1
            })
            this.generation_finished()
        })
      }
    

      generate_options(pre, new_options = false) {
        this.setState({
          sentence: pre.split(" "),
        })
        this.generation_started(false)
   
        fetch(`${BACKEND_URL}/api/generate_options`, {
          method: 'POST',
          body: JSON.stringify({
              'pre_sentence': pre,
              'new_options': new_options,
          }),
          headers: {
              "Content-type": "aplication/json; charset=UTF-8"
            }
        }).then(response => response.json())
        .then(message => {
            //console.log(message.sentences)
            this.setState({
              sentence: message.pre_sen.split(' '),
              sen_options: message.sentences,
            })
            this.generation_finished()
        })
      }
    
      option_choosed(opt_idx) {
        let pre_l = this.state.sentence.concat(this.state.sen_options[opt_idx])
        this.setState({
          sentence: pre_l,
          sen_options: []
        })
        let pre_sen = ''
        let i = 0
        for (let w of pre_l) {
          pre_sen += w
          if(i < pre_l.length-1) {
            pre_sen += ' '
          }
          i++
        }
        this.generate_options(pre_sen)
      }

      new_options() {
        this.setState({
          sen_options: [],
        })
        let pre_l = this.state.sentence
        let pre_sen = ''
        let i = 0
        for (let w of pre_l) {
          pre_sen += w
          if(i < pre_l.length-1) {
            pre_sen += ' '
          }
          i++
        }
        this.generate_options(pre_sen, true)
      }
    
    
      handle_typing(s) {
        let new_sentence = s.split(" ")
        this.setState({
          sentence: new_sentence,
          hasChanged: true,
        })
      }
      
    
      render() {
        return (
          <div>
              Baseline
          </div>
        );
      }
}

export default Baseline;
