import TextField from '../js_components/TextField'
import { OptionButtons } from '../js_components/OptionButtons'
import Baseline from './Baseline'

class Version2 extends Baseline {

    render() {
        this.props.set_length(this.state.sentence.length)
        return(
            <>
            <div>
                <TextField 
                    start={this.startClock} 
                    stop={this.stopClock}
                    on_submit={this.generate_options} 
                    sentence={this.state.sentence} 
                    handle_typing={this.handle_typing}
                    set_len={()=>{}}
                    disabled={this.state.isGenerating}
                />
            </div>
            <div>
                <OptionButtons
                    sentence_options={this.state.sen_options}
                    on_choose={this.option_choosed}
                    generate_new={this.new_options}
                    disabled={this.state.isGenerating}
                />
            </div>
            </>
        )
    }
}

export default Version2;