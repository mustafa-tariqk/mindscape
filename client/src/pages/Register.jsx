import React from 'react'
import Add from "../img/2.25+ KD Club logo.png"

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
                        <img src={Add} alt="cool image fuck yeah!"/>
                        <span>Add an Avatar</span>
                    </label>
                    <button>Sign Up</button>
                </form>
                <p>Already have an account? Log In</p>
            </div>
        </div>
    )
}

export default Register