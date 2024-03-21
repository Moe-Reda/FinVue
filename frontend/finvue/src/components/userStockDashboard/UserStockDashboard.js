import React, { useState, useEffect } from 'react';
import api from '../../api/axiosConfig';
import StockChart from '../stockChart/stockChart';
import './UserStockDashboard.css'; // Importing CSS file

const UserStockDashboard = ({ loggedIn }) => { // Using loggedIn instead of username
    const [stocks, setStocks] = useState([]);
    const [selectedStock, setSelectedStock] = useState('');
    const [stockData, setStockData] = useState([]);
    const [timeRange, setTimeRange] = useState('7'); // Default time range: 7 days
    const [modalOpen, setModalOpen] = useState(false);
    const [newStock, setNewStock] = useState({
        tick: '',
        order: '',
        quantity: ''
    });

    const fetchUserStocks = async () => {
        try {
            const response = await api.get(`http://127.0.0.1:5000/api/get_all_stocks/${loggedIn}`);
            setStocks(response.data.stocks);
        } catch (error) {
            console.error('Error fetching user stocks:', error);
        }
    };

    useEffect(() => {
        // Call fetchUserStocks inside useEffect
        fetchUserStocks();
    }, [loggedIn]);

    const fetchStockData = async (symbol, time) => {
        try {
            let response;
            if (symbol === 'Portfolio') {
                response = await api.get(`http://127.0.0.1:5000/api/get_portfolio_time_series/${loggedIn}/${time}`);
            } else {
                response = await api.get(`http://127.0.0.1:5000/api/get_time_series/${symbol}/${time}`);
            }
            setStockData(response.data.timeSeries);
        } catch (error) {
            console.error('Error fetching stock data:', error);
        }
    };

    const handleStockSelect = (event) => {
        const selectedSymbol = event.target.value;
        setSelectedStock(selectedSymbol);
        fetchStockData(selectedSymbol, timeRange);
    };

    const handleTimeRangeSelect = (event) => {
        const selectedTimeRange = event.target.value;
        setTimeRange(selectedTimeRange);
        fetchStockData(selectedStock, selectedTimeRange);
    };

    const openModal = () => {
        setModalOpen(true);
    };

    const closeModal = () => {
        setModalOpen(false);
    };

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setNewStock(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleAddStock = async () => {
        try {
            await api.post('http://127.0.0.1:5000/api/add_stock', {
                username: loggedIn,
                tick: newStock.tick,
                order: newStock.order,
                quantity: newStock.quantity
            });
            setModalOpen(false);
            setNewStock({
                tick: '',
                order: '',
                quantity: ''
            });
            fetchUserStocks();
        } catch (error) {
            console.error('Error adding stock:', error);
        }
    };


    return (
        <div className="user-stock-dashboard">
            <h2>Portfolio Dashboard</h2>
            <div className="time-range-dropdown">
                <label htmlFor="timeRange">Select Time Range:</label>
                <select id="timeRange" onChange={handleTimeRangeSelect}>
                    <option value="7">1 Week</option>
                    <option value="30">1 Month</option>
                    <option value="120">4 Months</option>
                    <option value="365">1 Year</option>
                </select>
            </div>
            <select className="stock-dropdown" value={selectedStock} onChange={handleStockSelect}>
                <option value="">Select an option</option>
                <option value="Portfolio">Portfolio</option>
                {stocks.map(stock => (
                    <option key={stock} value={stock}>{stock}</option> // Using stock as both key and value
                ))}
            </select>
            <button className="add-stock-button" onClick={openModal}>Add Stock</button>
            {modalOpen && (
                <div className="add-stock-modal">
                    <div className="add-stock-modal-content">
                        <span className="close" onClick={closeModal}>&times;</span>
                        <h3>Add Stock</h3>
                        <div className="form-group">
                            <label htmlFor="tick">Stock Symbol:</label>
                            <input type="text" id="tick" name="tick" value={newStock.tick} onChange={handleInputChange} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="order">Order Price:</label>
                            <input type="text" id="order" name="order" value={newStock.order} onChange={handleInputChange} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="quantity">Quantity:</label>
                            <input type="text" id="quantity" name="quantity" value={newStock.quantity} onChange={handleInputChange} />
                        </div>
                        <button onClick={handleAddStock}>Add</button>
                    </div>
                </div>
            )}
            {selectedStock && <StockChart data={stockData} symbol={selectedStock} />}
        </div>
    );
};

export default UserStockDashboard;
