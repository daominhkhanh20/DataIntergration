import axios from 'axios';

const baseUrl = "http://localhost:8888"

const guest = axios.create({ timeout: 30000 });

guest.defaults.withCredentials = true;

const Api = {
    searchByFilters: (filters) => {
        return Promise.resolve({
        })
    },
    getItems: (searchString ,currentPage, onlyGetMatchingData) => {
        return onlyGetMatchingData ? guest.get(`${baseUrl}/all_matching?page=${currentPage}&keyword=${searchString}`) : guest.get(`${baseUrl}/find?keyword=${searchString}&page=${currentPage}`)
    },
    getItem: (Id) => {
        return guest.get(`${baseUrl}/show/item?id=${Id}`)
    },
    getFilter: () => {
        return Promise.resolve({
            brandFilters: ["Asus", "Lenovo", "Apple", "Acer", "Dell", "HP", "MSI", "Razer", "Toshiba", "LG", "Microsoft", "Gigabyte", "Avita", "Samsung", "Xiaomi", "Fujitsu"],
            RAMFilters: ["4GB", "8GB", "16GB", "32GB", "64GB"],
            storageFilters: ["128GB", "256GB", "512GB", "1TB", "2TB"], 
        })
    }
}

export default Api
