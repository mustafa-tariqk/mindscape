import Neuma from '../img/Logo_with_subtext_upscaled.png'
import User from '../img/userprofile.png'

const Complete = () => {
    return (
        <div className='resultsScreen'>
            <div className='menubar'>
                <div className='left'>
                    <img src={Neuma} alt="Neuma Logo" />
                </div>
                <div className='middle'></div>
                <div className='right'>
                    <a href="#">Explore Experiences</a>
                    <a href="#">FAQ</a>
                    <img src={User} alt="Image" />
                </div>
            </div>
            {/* Now for the screen components*/}
            <div className='contribcontainer'>
                <div className='bigtitle'>Thank you for your contribution!</div>
                <div className='subtitle'>Below are your results</div>
                <div className="grid-container">
                   <span>World Cloud</span>
                   <span>Experience Similarity</span>
                   <span>Experience Class</span>
                </div>
                <div className='imagebutton'>
                    <button>Download Image</button>
                </div>
                <div className='feedbackbutton'>
                    <button>Submit Feedback</button>
                </div>
            </div>
        </div>
    )
}

export default Complete