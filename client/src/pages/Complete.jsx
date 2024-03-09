import React from 'react';
import WordCloud from 'react-d3-cloud';
import GridList from '../components/GridList.jsx';
import PieChart from '../components/PieChart.jsx';
import {Chart, ArcElement, Tooltip, Legend} from 'chart.js'
Chart.register(ArcElement);
Chart.register(Tooltip);
Chart.register(Legend);
import { useState, useEffect } from 'react';

const SERVER_URL = process.env.SERVER_URL;

const tempdata = [
    { text: '  ', value: 1000 }
];

const piechartData = {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [
      {
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor: [
          'red',
          'blue',
          'yellow',
          'green',
          'purple',
          'orange',
        ],
        borderWidth: 1,
      },
    ],
};

const experienceClassData = null

const Complete = ({chatId}) => {

    // PRIORITY 1
    if (!chatId) {
        console.error("Chat ID is not set.");
        return;
    }

    const [experienceClassData, setExperienceClassData] = useState([]);
    const [wordCloudData, setWordCloudData] = useState([]);

    useEffect(() => {
        //Experience Data
        fetch(SERVER_URL+'/api/submit', {
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({chatId})
        })
        .then(response => response.json())
        .then(data => {
            setExperienceClassData(data)
        });
        //WordCloud data
        fetch(SERVER_URL + "/api/analytics/get_frequent_words?" + new URLSearchParams({
            chat_id: chatId,
            k: 25,
        }), {
            method: 'GET',
            mode: 'cors',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            setWordCloudData(data)
        });
    }, [chatId]);

    function printDebug() {
        //console.log(experienceClassData)
        console.log(wordCloudData)
        const type = typeof wordCloudData
        console.log('Data is of type:', type);
    }

    const transformWordData = () => {
        if(typeof wordCloudData != "string")
        {
            console.log("BRUH")
            return tempdata
        }
        const modified = JSON.parse(wordCloudData);
        const newData = []
        for (const key in modified) {
            const newObject = { text: key, value: Math.max(parseInt(0.355 * (Math.pow(modified[key].weight, -4)) - 148244), 10) }
            // console.log(key);
            // console.log(modified[key].weight)
            newData.push(newObject)
        }
        console.log(newData)
        return newData;
    }

    return (
        <div className='bg'>
            <div className='resultsScreen'>
                {/* Now for the screen components*/}
                <div className='contribcontainer'>
                    <div className='bigtitle'>Thank you for your contribution!</div>
                    <div className='subtitle'>Below are your results</div>
                    <div className='graphs'>
                        <div className='wordCloud'>
                            <WordCloud
                            className="wordCloud"
                            data={transformWordData()}
                            width={500}
                            height={500}
                            font="Times"
                            fontStyle="italic"
                            fontWeight="bold"
                            fontSize={(word) => (word.value) / 2}
                            spiral="rectangular"
                            rotate={(word) => Math.random(word.value) * 180 - 90}
                            padding={5}
                            random={Math.random}
                            />
                        </div>
                        <div className='similarity'>
                            <div className='pieChartStyle'>
                                <PieChart data={piechartData} />
                            </div>
                        </div>
                        <div className='experience'>
                            {/* First Grid is for Dosage Information*/}
                            <GridList items={[["DOSE:", "UNIT:", "METHOD:", "SUBSTANCE:", "SHAPE:"], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]}/>
                            {/* Second Grid is for user information*/}
                            <GridList items={[["INFO-","HEIGHT:", "RESULT", "WEIGHT:", "RESULT"], [0,0,0,0,0]]}/>
                        </div>
                    </div>
                    <div className="grid-container">
                    <span>Word Cloud</span>
                    <span>Experience Similarity</span>
                    <span>Experience Class</span>
                    </div>
                    <div className='imagebutton'>
                        <button onClick={printDebug}>Download Image</button>
                    </div>
                    <div className='feedbackbutton'>
                        <button onClick={printDebug}>Submit Feedback</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Complete