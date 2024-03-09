import Neuma from '../img/Logo_with_subtext_upscaled.png'
import User from '../img/userprofile.png'
import Wellness from '../img/wellness_background.png'
import React from 'react'

const SERVER_URL = process.env.SERVER_URL;

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
                            Disclaimer: Website Usage and Privacy Policy

                            1. Introduction

                            Thank you for visiting our website. By using this
                            website, you agree to comply with and be bound by
                            the following terms and conditions of use, which
                            together with our privacy policy govern your
                            relationship with this website. If you disagree
                            with any part of these terms and conditions, please
                            refrain from using our website.

                            2. Acceptance of Terms

                            By accessing this website, you acknowledge that you
                            have read, understood, and agree to be bound by all
                            terms and conditions contained herein. These terms
                            and conditions, along with our privacy policy,
                            govern your use of this website, including all
                            content, services, and products available through
                            this website.

                            3. Cookies

                            This website uses cookies to enhance user experience
                            and functionality. By accepting our use of cookies,
                            you agree to allow us to store and access cookies
                            on your device. Cookies are small pieces of data
                            stored on your device that help us improve the
                            performance and usability of our website. You have
                            the option to decline our use of cookies, although
                            this may limit the functionality of certain parts
                            of our website.

                            4. Psychedelics Disclaimer

                            This website strictly prohibits the promotion, sale,
                            or use of illegal substances, including but not
                            limited to psychedelics. It is your responsibility
                            to comply with all applicable laws and regulations
                            regarding the use of controlled substances. Any
                            information provided on this website regarding
                            psychedelics is for informational purposes only
                            and should not be construed as encouragement or
                            endorsement of illegal activities.

                            5. Privacy Policy

                            Your privacy is important to us. This website
                            collects and processes personal information in
                            accordance with our privacy policy. By using this
                            website, you consent to the collection, storage, and
                            processing of your personal information as outlined
                            in our privacy policy. We take reasonable measures
                            to protect the security and confidentiality of your
                            personal information, but we cannot guarantee
                            absolute security against unauthorized access or
                            disclosure.

                            6. Information Access

                            By using this website, you acknowledge and consent
                            to the fact that researchers and administrators
                            associated with this website may have access to your
                            information for research, analysis, and
                            administrative purposes. We take your privacy
                            seriously and will only use your information in
                            accordance with our privacy policy.

                            7. Amendments

                            We reserve the right to amend these terms and
                            conditions and our privacy policy at any time
                            without prior notice. It is your responsibility to
                            review these terms and conditions periodically to
                            stay informed of any changes. Your continued use of
                            this website constitutes acceptance of any
                            amendments to these terms and conditions.

                            8. Governing Law

                            These terms and conditions shall be governed by and
                            construed in accordance with the laws of
                            [jurisdiction]. Any dispute arising out of or
                            related to these terms and conditions shall be
                            subject to the exclusive jurisdiction of the courts
                            of [jurisdiction].

                            9. Contact Information

                            If you have any questions or concerns regarding
                            these terms and conditions or our privacy policy,
                            please contact us at [contact information].

                            By using this website, you agree to the terms and
                            conditions outlined above. Thank you for visiting
                            our website.

                        </p>
                        <button>Sign in with Google</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login;