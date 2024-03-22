import React from 'react';
import WordCloud from 'react-d3-cloud';
import GridList from '../components/GridList.jsx';
import PieChart from '../components/PieChart.jsx';
import {Chart, ArcElement, Tooltip, Legend} from 'chart.js';
Chart.register(ArcElement);
Chart.register(Tooltip);
Chart.register(Legend);
import { useState, useEffect } from 'react';
import simScale from "../img/simScale.png";

const SERVER_URL = process.env.SERVER_URL;

const tempdata = [
    { text: '  ', value: 1000 }
];

const piechartData = {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [
      {
        label: '# of Votes',
        data: [100],
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

const Complete = ({chatId}) => {

    // PRIORITY 1
    if (!chatId) {
        console.error("Chat ID is not set.");
        return;
    }

    const [experienceClassData, setExperienceClassData] = useState([]);
    const [wordCloudData, setWordCloudData] = useState([]);
    const [emotionalExperienceData, setEmotionalExperienceData] = useState([]);

    useEffect(() => {
        //Experience Data
        fetch(SERVER_URL+'/api/submit', {
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({chatId, test: true})
            // body: JSON.stringify({chatId, test: true})
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
        //Emotional Data
        fetch(SERVER_URL + "/api/analytics/experience?" + new URLSearchParams({
            test: true,
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
            setEmotionalExperienceData(data)
        });
    }, [chatId]);

    function printDebug() {
        //console.log(experienceClassData)
        console.log(emotionalExperienceData)
        const type = typeof emotionalExperienceData
        console.log('Data is of type:', type);
    }

    const transformWordData = () => {
        if(typeof wordCloudData != "string" || Object.keys(wordCloudData).length < 500)
        {
            console.log("BRUH")
            return tempdata
        }
        const modified = JSON.parse(wordCloudData);
        // Find the biggest and smallest values
        var biggestVal = -(Infinity)
        var smallestVal = Infinity

        for (const key1 in modified) {
            if(modified[key1].weight > biggestVal) { biggestVal = modified[key1].weight; }
            if(modified[key1].weight < smallestVal) { smallestVal = modified[key1].weight; }
        }
        console.log("Biggest val is " + biggestVal);
        console.log("Smallest val is " + smallestVal);
        // Normalize Values

        var workingValues = structuredClone(modified)
        const workingKeys = Object.keys(modified);

        // Iterate over the keys using a regular for loop
        const maxSize = 150;
        var randoTick = maxSize;
        const minSize = 25;
        for (let i = 0; i < workingKeys.length; i++) {
            if (i == 0) { workingValues[Object.keys(workingValues)[0]].weight = maxSize}
            else {
                var max = (maxSize / workingKeys.length) * 1.75;
                var min = (maxSize / workingKeys.length) * 0.75;
                randoTick = randoTick - (Math.floor(Math.random() * (max - min + 1)) + min);
                workingValues[Object.keys(workingValues)[i]].weight = Math.max(minSize, randoTick);
            }
        }

        const newData = []
        for (const key in modified) {
            const newObject = { text: key, value: workingValues[key].weight }
            // Math.max(parseInt(0.355 * (Math.pow(modified[key].weight, -4)) - 148244), 10)
            // console.log(key);
            // console.log(modified[key].weight)
            newData.push(newObject)
        }
        console.log(newData)
        return newData;
    }

    const createClassificationData = () => {
        //Default Value
        var temp = [["HEIGHT(CM):", "SUBSTANCE:", "WEIGHT(KG):"]];

        const catNames = [];
        for (const key in experienceClassData) {
            catNames.push(key);
        }

        if (catNames != []) {
            temp = [catNames]
        } 

        if (experienceClassData.length == 0) {
            return [["HEIGHT:", "SUBSTANCE:", "WEIGHT:"]];
        }

        const additions = []
        for (const key in experienceClassData) {
            console.log(key);
            additions.push(experienceClassData[key]);
        }
        temp.push(additions);
        return temp;
    }

    const openGoogleForm = () => {
        const url = "https://forms.gle/orEBNU7GmVLKpmJe7";
        window.open(url, "_blank")
    }

    const createPieChartData = () => {
        if (emotionalExperienceData == null) {
            return piechartData;
        }

        var tempNames = []
        var tempValues = []
        var tempSim = []
        //Get the names and values of the passed
        for (const key in emotionalExperienceData['experiences']) {
            tempNames.push(emotionalExperienceData['experiences'][key]['name']);
            tempValues.push(emotionalExperienceData['experiences'][key]['percentage']);
            tempSim.push(emotionalExperienceData['experiences'][key]['similarity']);
        }
        
        var colors = []
        //var counter = 1;
        //make a list of colors using the simularity as the vibrance.
        for (const key in tempSim) {
            var simSat = 250 - (Math.min(Math.floor(tempSim[key] / 1.25 - 15, 250)));
            //var rand = Math.floor(Math.random() * 360);
            colors.push(`hsl(${simSat}, 100%, 50%)`);
        }

        console.log(colors);

        const newChart = {
            type: 'doughnut',
            labels: tempNames,
            borderColor: '#000000',
            datasets: [
              {
                label: 'Appears in X% of Submissions',
                data: tempValues,
                backgroundColor: colors,
                borderWidth: 4,
                borderColor: '#000000',
                hoverOffset: 10,
                hoverBorderWidth: 10,
                cutout: 50,
              },
            ],
        };

        return newChart;
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
                            <div className='pieChartInfo'>See similarity range below!</div>
                            <img src={simScale}></img>
                            <div className='pieChartStyle'>
                                <PieChart data={createPieChartData()} />
                            </div>
                        </div>
                        <div className='experience'>
                            {/* First Grid is for Dosage Information*/}
                            <GridList items={createClassificationData()}/>
                        </div>
                    </div>
                    <div className="grid-container">
                    <span>Word Cloud</span>
                    <span>Experience Similarity</span>
                    <span>Constributor Info</span>
                    </div>
                    <div className='imagebutton'>
                        {/* <button onClick={printDebug}>Download Image</button> */}
                    </div>
                    <div className='feedbackbutton'>
                        <button onClick={openGoogleForm}>Submit Feedback</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Complete