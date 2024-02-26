import React from 'react';
import '../App.css';
import { to_string, BACKEND_URL } from '../App'

class TextField extends React.Component{

  constructor(props) {
    super(props)
    this.state = {
      intervalId: -1,
      amountBack: 0,
    }
  }

  handleTyping(event) {
    event.preventDefault()
    this.props.stop()

    this.props.set_len(event.target.value.split(' ').length)

    fetch(`${BACKEND_URL}/api/task/log_input`, {
      method: 'POST',
      body: JSON.stringify({
          'sentence': event.target.value
      }),
      headers: {
          "Content-type": "aplication/json; charset=UTF-8"
        }
    })

    this.props.handle_typing(event.target.value)

    if(this.state.intervalId !== -1) {
      clearInterval(this.state.intervalId)
    }
    this.setState({intervalId: setInterval(this.apply_changes.bind(this), 2000)})
  }

  handleSubmit(event) {
    event.preventDefault()
    this.apply_changes()
  }

  apply_changes() {
    if(this.state.intervalId !== -1) {
      clearInterval(this.state.intervalId)
      this.setState({intervalId: -1})
    }
    let sentence = document.getElementById('field').value
    this.props.on_submit(sentence)
  }

  componentWillUnmount() {
    clearInterval(this.state.intervalId)

    fetch(`${BACKEND_URL}/api/task/store_result`, {
      method: 'POST',
      body: JSON.stringify({
          'result': to_string(this.props.sentence)
      }),
      headers: {
          "Content-type": "aplication/json; charset=UTF-8"
        }
    })
  }

  // onBlur={this.props.start} 
  render() {
    return (
      <>
        <form onSubmit={this.handleSubmit.bind(this)}>
          <textarea id='field' type='text' className="TextField" 
                    value={to_string(this.props.sentence)} 
                    onChange={this.handleTyping.bind(this)} 
                    onFocus={this.props.stop}
                    disabled={this.props.disabled}> 
          </textarea>
        </form>
      </>
    );
  }
}

export default TextField;