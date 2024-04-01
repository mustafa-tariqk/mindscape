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
import axios from 'axios'

const SERVER_URL = process.env.SERVER_URL;

//Temporary Data for the word cloud, loaded when the wordcloud recieves no data
const tempdata = [
    { text: '  ', value: 1000 }
];

//Temporary pie chart data, loaded when pie chart recieves nothing
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
/*
Name: Complete
Functionality: Complete loads rewards data and draws it accordingly
Intake: chatId
Returns: Formatted Page
*/
const Complete = ({chatId}) => {

    // PRIORITY 1
    if (!chatId) {
        console.error("Chat ID is not set.");
        return;
    }

    //Initialize reward data
    const [categoryData, setCategoryData] = useState({});
    const [wordCloudData, setWordCloudData] = useState([]);
    const [experienceData, setExperienceData] = useState([]);
    const [categoriesLoading, setCategoriesLoading] = useState(true);
    const [wordCloudLoading, setWordCloudLoading] = useState(true);
    const [experienceLoading, setExperienceLoading] = useState(true);

    useEffect(() => {
        axios.post(
            SERVER_URL + '/api/submit',
            { chatId /*, test: true */ },
            {
                timeout: 0,
                mode: 'cors',
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        ).then((response) => {
            setCategoryData(response.data);
            setCategoriesLoading(false);
        }).catch((error) => {
            console.error('Error:', error.message);
        })
    }, [chatId]);

    //Use Effect calls the data from the server when the chatID is updated/passed. (On load)
    useEffect(() => {
        if (Object.keys(categoryData).length == 0) { return; }
        // Only happens once submit has been completed
        // wordCloud data
        axios.get(
            SERVER_URL + '/api/analytics/get_frequent_words',
            {
                params: {
                chat_id: chatId,
                k: 25,
                //test: true,
                },
                timeout: 0,
                mode: 'cors',
                withCredentials: true,
                headers: {
                'Content-Type': 'application/json'
                }
            }
        ).then((response) => { 
            setWordCloudData(response.data);
            setWordCloudLoading(false);
        }).catch((error) => {
            console.error('Error:', error.message);
        });
        
        // experience Data
        axios.get(
        `${SERVER_URL}/api/analytics/experience`,
        {
            params: {
            chat_id: chatId,
            k: 3,
            //test: true,
            },
            timeout: 0,
            mode: 'cors',
            withCredentials: true,
            headers: {
            'Content-Type': 'application/json'
            }
        }
        ).then((response) => {
        setExperienceData(response.data);
        setExperienceLoading(false);
        }).catch((error) => { 
        console.error('Error:', error.message);
        });
    }, [categoryData]);


    /*
    Name: printDebug
    Functionality: Used for testing, prints data types and values
    Intake: --
    Returns: --
    */
    function printDebug() {
        //console.log(experienceClassData)
        console.log(experienceData)
        const type = typeof experienceData
        console.log('Data is of type:', type);
    }

    /*
    Name: transformWordData
    Functionality: Gets the wordcloud data from analtics, and determines the size of words using said data.
    Intake: --
    Returns: A list of words along with their sizes, to be used on chart initialization
    */
    const transformWordData = () => {
        if(typeof wordCloudData != "string" || Object.keys(wordCloudData).length < 500)
        {
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

    /*
    Name: createClassificationData
    Functionality: Creates the data for the user information table, scales with table size
    Intake: --
    Returns: A list of lists of strings
    */
    const createClassificationData = (data) => {
        if (Object.keys(data).length == 0) { return [["No data found or still loading"]]}
        // load headers
        let result = [Object.keys(data["submitter_info"][0])]

        if (result[0].length == 0) {
            return [["No data found or still loading"]]
        }
        
        // submitter's information
        let row = []
        for (const key of result[0]) {
            if (key in data["submitter_info"]) {
                row.push(data["submitter_info"][key])
            } else {
                row.push("N/A")
            }
        }
        result.push(row) // only 1 row

        // substance information, potential issue if the substances do not have the same keys
        result.push(Object.keys(data["substance_info"][0]))
        for (const substance of data["substance_info"]) {
            row = []
            for (const key in substance) {
                if (key in substance) {
                    row.push(substance[key])
                } else {
                    row.push("N/A")
                }
            }
            result.push(row)
        }
        console.log(result)
        return result
    }

    /*
    Name: openGoogleForm
    Functionality: Opens up the google form for feedback. called when feedback button is pressed
    Intake: --
    Returns: --
    */
    const openGoogleForm = () => {
        const url = "https://forms.gle/orEBNU7GmVLKpmJe7";
        window.open(url, "_blank")
    }

    /*
    Name: createPieChartData
    Functionality: creates the data or the piechart. calculates the colors for the chart from passed similarity values
    Intake: --
    Returns: Fully ready to be drawn chart with all required data
    */
    const createPieChartData = () => {
        if (experienceData == null) {
            return piechartData;
        }

        var tempNames = []
        var tempValues = []
        var tempSim = []
        //Get the names and values of the passed
        for (const key in experienceData['experiences']) {
            tempNames.push(experienceData['experiences'][key]['name']);
            tempValues.push(experienceData['experiences'][key]['percentage']);
            tempSim.push(experienceData['experiences'][key]['similarity']);
        }
        
        var colors = []
        //var counter = 1;
        //make a list of colors using the simularity as the vibrance.

        //Get the sum so we can normalize
        var totalSum = 0;
        for (const col in tempSim) {
            totalSum += tempSim[col];
        }

        for (const key in tempSim) {
            //var simSat = 250 - (Math.min(Math.floor(tempSim[key] / 1.25 - 15, 250)));
            //var rand = Math.floor(Math.random() * 360);
            var simSat = (tempSim[key] / totalSum * 250);
            colors.push(`hsl(${simSat}, 100%, 50%)`);
        }

        //console.log(colors);

        // Create new chart using data and return it
        const newChart = {
            type: 'doughnut',
            labels: tempNames,
            borderColor: '#000000',
            datasets: [
              {
                label: "Found in X% of Submissions",
                data: tempValues,
                backgroundColor: colors,
                borderWidth: 4,
                borderColor: '#000000',
                hoverOffset: 50,
                hoverBorderWidth: 10,
                radius: '70%',
                cutout: '35%',
              },
            ],
            options: {
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        };

        return newChart;
    }

    //Black magic deep dark manipulations
    Chart.overrides["doughnut"].plugins.legend.display = false;
    Chart.overrides["pie"].plugins.legend.display = false;

    //Final return statement
    return (
        <div className='bg'>
            <div className='resultsScreen'>
                {/* Now for the screen components*/}
                <div className='contribcontainer'>
                    <div className='bigtitle'>Thank you for your contribution!</div>
                    <div className='subtitle'>Below are your results</div>
                    <div className='graphs'>
                        <div className='wordCloud'>
                            <p>{wordCloudLoading ? 'LOADING...' : null}</p>
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
                            <p>{experienceLoading ? 'LOADING...' : null}</p>
                                <PieChart data={createPieChartData()}/>
                            </div>
                        </div>
                        <div className='experience'>
                            {/* First Grid is for Dosage Information*/}
                            <p>{categoriesLoading ? 'LOADING...' : null}</p>
                            <GridList items={createClassificationData(categoryData)}/>
                        </div>
                    </div>
                    <div className="grid-container">
                    <span>Word Cloud</span>
                    <span>Experience Similarity</span>
                    <span>Contributor Info</span>
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
