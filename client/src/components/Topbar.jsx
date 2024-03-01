import image1 from '../img/Logo_with_subtext_upscaled.png'
import image2 from '../img/userprofile.png'

const Topbar = () => {
    return (
        <div className="topbar">
          <div className="left">
            <img src={image1} alt="Image 1" />
          </div>
          <div className="gap"></div>
          <div className="right">
            <a href="#">Explore Experiences</a>
            <a href="#">FAQ</a>
            <img src={image2} alt="Image 2" />
          </div>
        </div>
      );
}

export default Topbar;