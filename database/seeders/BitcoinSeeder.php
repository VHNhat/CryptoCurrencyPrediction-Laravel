<?php

// namespace Database\Seeders;

// use App\Models\Bitcoin;
// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
// use Illuminate\Database\Seeder;
// use File;

// class BitcoinSeeder extends Seeder
// {
//     /**
//      * Run the database seeds.
//      *
//      * @return void
//      */
//     public function run()
//     {
//         $json = File::get(public_path("bitcoin.json"));
//         $bitcoins = json_decode($json);
        
//         foreach ($bitcoins->bitcoins as $key => $value) {
//             Bitcoin::create([
//                 "date" => $value->date,
//                 "actual_closing_price" => $value->actual_closing_price,
//                 "pred_closing_price" => $value->pred_closing_price
//             ]);
//         }
//     }
// }
