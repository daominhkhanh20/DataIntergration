import axios from 'axios';

// const baseUrl = "http://localhost:3001"

const guest = axios.create({ timeout: 30000 });

guest.defaults.withCredentials = true;

const Api = {
    searchByFilters: (filters) => {
        return Promise.resolve({
        })
    },
    getItems: (currentPage, searchString ,pageSize) => {
        return Promise.resolve({
            totalPage: 10,
            currentPage: currentPage,
            items: [
                {
                    id: 1,
                    name: "Laptop HP Pavilion 15 eg0541TU i3 1125G4/4GB/512GB/Win11 (4P5G8PA) ",
                    price: 100000,
                    brand: "Asus",
                    CPU: "i5-12000H",
                    GPU: "Intel Iris Xe Graphics",
                    RAM: 8,
                    storage: 256,
                    shopNum: 2
                },
                {
                    id: 2,
                    name: "Laptop HP Pavilion 15 eg0541TU i3 1125G4/4GB/512GB/Win11 (4P5G8PA) ",
                    price: 100000,
                    brand: "Asus",
                    CPU: "i5-12000H",
                    GPU: "Intel Iris Xe Graphics",
                    RAM: 8,
                    storage: 256,
                    shopNum: 2
                },
                {
                    id: 3,
                    name: "Laptop HP Pavilion 15 eg0541TU i3 1125G4/4GB/512GB/Win11 (4P5G8PA) ",
                    price: 100000,
                    brand: "Asus",
                    CPU: "i5-12000H",
                    GPU: "Intel Iris Xe Graphics",
                    RAM: 8,
                    storage: 256,
                    shopNum: 2
                },
                {
                    id: 4,
                    name: "Laptop HP Pavilion 15 eg0541TU i3 1125G4/4GB/512GB/Win11 (4P5G8PA) ",
                    price: 100000,
                    brand: "Asus",
                    CPU: "i5-12000H",
                    GPU: "Intel Iris Xe Graphics",
                    RAM: 8,
                    storage: 256,
                    shopNum: 2
                },
                {
                    id: 5,
                    name: "Laptop HP Pavilion 15 eg0541TU i3 1125G4/4GB/512GB/Win11 (4P5G8PA) ",
                    price: 100000,
                    brand: "Asus",
                    CPU: "i5-12000H",
                    GPU: "Intel Iris Xe Graphics",
                    RAM: 8,
                    storage: 256,
                    shopNum: 2
                },
                {
                    id: 6,
                    name: "Laptop HP Pavilion 15 eg0541TU i3 1125G4/4GB/512GB/Win11 (4P5G8PA) ",
                    price: 100000,
                    brand: "Asus",
                    CPU: "i5-12000H",
                    GPU: "Intel Iris Xe Graphics",
                    RAM: 8,
                    storage: 256,
                    shopNum: 2
                },
                {
                    id: 7,
                    name: "Laptop HP Pavilion 15 eg0541TU i3 1125G4/4GB/512GB/Win11 (4P5G8PA) ",
                    price: 100000,
                    brand: "Asus",
                    CPU: "i5-12000H",
                    GPU: "Intel Iris Xe Graphics",
                    RAM: 8,
                    storage: 256,
                    shopNum: 2
                },
                {
                    id: 8,
                    name: "Laptop HP Pavilion 15 eg0541TU i3 1125G4/4GB/512GB/Win11 (4P5G8PA) ",
                    price: 100000,
                    brand: "Asus",
                    CPU: "i5-12000H",
                    GPU: "Intel Iris Xe Graphics",
                    RAM: 8,
                    storage: 256,
                    shopNum: 2
                },
                {
                    id: 9,
                    name: "Laptop HP Pavilion 15 eg0541TU i3 1125G4/4GB/512GB/Win11 (4P5G8PA) ",
                    price: 100000,
                    brand: "Asus",
                    CPU: "i5-12000H",
                    GPU: "Intel Iris Xe Graphics",
                    RAM: 8,
                    storage: 256,
                    shopNum: 2
                }
            ]
        })
    },
    getItem: (Id) => {
        return Promise.resolve({

        })
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
