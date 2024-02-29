import React from 'react'
import User from "../img/userprofile.png";

const Register = () => {
    return (
        <div className='formContainer'>
            <div className = "formWrapper">
                <span className='logo'>Lama Chat</span>
                <span className='title'>Register</span>
                <form>
                    <input type="text" placeholder='Display Name'/>
                    <input type="email" placeholder='email'/>
                    <input type="password" placeholder='password'/>
                    <input style={{display:"none"}} type="file" id="file"/>
                    <label htmlFor='file'>
                        <img src={User} alt="cool image fuck yeah!"/>
                        <span>User an Avatar</span>
                    </label>
                    <button>Sign Up</button>
                </form>
                <p>Already have an account? Log In</p>
            </div>
        </div>
    )
}

export default Register