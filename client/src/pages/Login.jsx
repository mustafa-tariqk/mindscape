import Neuma from '../img/Logo_with_subtext_upscaled.png'
import User from '../img/userprofile.png'
import Wellness from '../img/wellness_background.png'

const Login = () => {
    return (
        <div className='agreementScreen'>
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
            <div className="page">
                <div className="background">
                    <img src={Wellness} alt="A Tranquil Background" />
                    <div className="content">
                        <h1>NEUMA Mindscape</h1>
                        <h2>Conversational AI Chatbot</h2>
                        <p>
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla
                            condimentum tortor eu risus convallis, nec aliquet odio vestibulum.
                            Nullam vehicula urna ac lacinia consequat.
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla
                            condimentum tortor eu risus convallis, nec aliquet odio vestibulum.
                            Nullam vehicula urna ac lacinia consequat.
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla
                            condimentum tortor eu risus convallis, nec aliquet odio vestibulum.
                            Nullam vehicula urna ac lacinia consequat.
                            By signing in, you accept these terms and conditions.
                        </p>
                        <button>Sign in with Google</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login;