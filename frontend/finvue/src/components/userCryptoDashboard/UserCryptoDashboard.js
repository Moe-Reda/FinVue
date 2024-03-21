import React, { useState, useEffect } from 'react';
import api from '../../api/axiosConfig';
import StockChart from '../stockChart/stockChart';
import './UserCryptoDashboard.css'; // Importing CSS file

const UserCryptoDashboard = ({ loggedIn }) => { // Using loggedIn instead of username
    const [cryptos, setCryptos] = useState([]);
    const [selectedCrypto, setSelectedCrypto] = useState('');
    const [cryptoData, setCryptoData] = useState([]);
    const [timeRange, setTimeRange] = useState('7'); // Default time range: 7 days
    const [modalOpen, setModalOpen] = useState(false);
    const [newCrypto, setNewCrypto] = useState({
        tick: '',
        order: '',
        quantity: ''
    });

    const fetchUserCryptos = async () => {
        try {
            const response = await api.get(`http://127.0.0.1:5000/api/get_all_cryptos/${loggedIn}`);
            setCryptos
    (response.data.cryptos);
        } catch (error) {
            console.error('Error fetching user cryptos:', error);
        }
    };

    useEffect(() => {
        // Call fetchUserCryptos inside useEffect
        fetchUserCryptos();
    }, [loggedIn]);

    const fetchCryptoData = async (symbol, time) => {
        try {
            let response;
            if (symbol === 'Portfolio') {
                response = await api.get(`http://127.0.0.1:5000/api/get_crypto_portfolio_time_series/${loggedIn}/${time}`);
            } else {
                response = await api.get(`http://127.0.0.1:5000/api/get_crypto_time_series/${symbol}/${time}`);
            }
            setCryptoData(response.data.timeSeries);
        } catch (error) {
            console.error('Error fetching crypto data:', error);
        }
    };

    const handleCryptoSelect = (event) => {
        const selectedSymbol = event.target.value;
        setSelectedCrypto(selectedSymbol);
        fetchCryptoData(selectedSymbol, timeRange);
    };

    const handleTimeRangeSelect = (event) => {
        const selectedTimeRange = event.target.value;
        setTimeRange(selectedTimeRange);
        fetchCryptoData(selectedCrypto, selectedTimeRange);
    };

    const openModal = () => {
        setModalOpen(true);
    };

    const closeModal = () => {
        setModalOpen(false);
    };

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setNewCrypto(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleAddCrypto = async () => {
        try {
            await api.post('http://127.0.0.1:5000/api/add_crypto', {
                username: loggedIn,
                tick: newCrypto.tick,
                order: newCrypto.order,
                quantity: newCrypto.quantity
            });
            setModalOpen(false);
            setNewCrypto({
                tick: '',
                order: '',
                quantity: ''
            });
            fetchUserCryptos();
        } catch (error) {
            console.error('Error adding crypto:', error);
        }
    };


    return (
        <div className="user-crypto-dashboard">
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
            <select className="crypto-dropdown" value={selectedCrypto} onChange={handleCryptoSelect}>
                <option value="">Select an option</option>
                <option value="Portfolio">Portfolio</option>
                {cryptos.map(crypto => (
                    <option key={crypto} value={crypto}>{crypto}</option> // Using crypto as both key and value
                ))}
            </select>
            <button className="add-crypto-button" onClick={openModal}>Add Crypto</button>
            {modalOpen && (
                <div className="add-crypto-modal">
                    <div className="add-crypto-modal-content">
                        <span className="close" onClick={closeModal}>&times;</span>
                        <h3>Add Crypto</h3>
                        <div className="form-group">
                            <label htmlFor="tick">Crypto Symbol:</label>
                            <input type="text" id="tick" name="tick" value={newCrypto.tick} onChange={handleInputChange} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="order">Order Price:</label>
                            <input type="text" id="order" name="order" value={newCrypto.order} onChange={handleInputChange} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="quantity">Quantity:</label>
                            <input type="text" id="quantity" name="quantity" value={newCrypto.quantity} onChange={handleInputChange} />
                        </div>
                        <button onClick={handleAddCrypto}>Add</button>
                    </div>
                </div>
            )}
            {selectedCrypto && <StockChart data={cryptoData} symbol={selectedCrypto} />}
        </div>
    );
};

export default UserCryptoDashboard;
