import Neuma from '../img/Logo_with_subtext_upscaled.png';
import User from '../img/userprofile.png';
import React, { useEffect } from 'react';
import { render } from 'react-dom';
import WordCloud from 'react-d3-cloud';
import GridList from '../components/GridList';

const data = [
    { text: 'Hey', value: 1000 },
    { text: 'lol', value: 200 },
    { text: 'first impression', value: 800 },
    { text: 'very cool', value: 1000000 },
    { text: 'duck', value: 10 },
];

const Complete = () => {
    useEffect(() => {
        //generateWordCloud();
    }, []);

    const generateWordCloud = () => {
        render (
            <WordCloud
                className="wordCloud"
                data={data}
                width={500}
                height={500}
                font="Times"
                fontStyle="italic"
                fontWeight="bold"
                fontSize={(word) => Math.log2(word.value) * 5}
                spiral="rectangular"
                rotate={(word) => word.value % 360}
                padding={5}
                random={Math.random}
            />,
            document.getElementById('root')
        )
        console.log("Image Generated");
    }

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
                <div className='graphs'>
                    <div className='wordCloud'>
                        <WordCloud
                        className="wordCloud"
                        data={data}
                        width={500}
                        height={500}
                        font="Times"
                        fontStyle="italic"
                        fontWeight="bold"
                        fontSize={(word) => Math.log2(word.value) * 5}
                        spiral="rectangular"
                        rotate={(word) => word.value % 360}
                        padding={5}
                        random={Math.random}
                        />
                    </div>
                    <div className='similarity'></div>
                    <div className='experience'>
                        {/* First Grid is for Dosage Information*/}
                        <GridList items={[["DOSE:", "UNIT:", "METHOD:", "SUBSTANCE:", "SHAPE:"], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]}/>
                        {/* Second Grid is for user information*/}
                        <GridList items={[["INFO-","HEIGHT:", "RESULT", "WEIGHT:", "RESULT"], [0,0,0,0,0]]}/>
                    </div>
                </div>
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