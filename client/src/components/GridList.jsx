import React from 'react';

const GridItem = ({ cellValues }) => {
  return (
    <div className="grid-item">
      {/* Render each cell with its respective value */}
      {cellValues.map((value, index) => (
        <div key={index} className="cell">
          {value}
        </div>
      ))}
    </div>
  );
};

const GridList = ({ items }) => {
  return (
    <div className="grid-list">
      {/* Render each grid item */}
      {items.map((item, index) => (
        <GridItem key={index} cellValues={item} />
      ))}
    </div>
  );
};

export default GridList;