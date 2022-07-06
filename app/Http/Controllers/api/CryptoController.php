<?php

namespace App\Http\Controllers\api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\Crypto;
use App\Models\Bitcoin;
use App\Models\Ethereum;
use App\Models\XRP;
use phpDocumentor\Reflection\PseudoTypes\LowercaseString;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class CryptoController extends Controller
{
    public $restful = true;
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index($coin)
    {
        //
        $coin = strtolower($coin);
        if($coin == 'bitcoin' || $coin == 'ethereum' || $coin == 'xrp'){
            $process = new Process(['python', 'App/main.py', $coin]);
            $process->run();

            // error handling
            if (!$process->isSuccessful()) {
                throw new ProcessFailedException($process);
            }

            // Get the contents of the JSON file 
            $strJsonFileContents = file_get_contents($coin.".json");
            $jsonResult = json_decode($strJsonFileContents);

            // Add json to database
            if($coin == 'bitcoin'){
                Bitcoin::truncate();
                foreach ($jsonResult->bitcoin as $key => $value) {
                    Bitcoin::create([
                        "date" => date('Y-m-d',strtotime($value->Date)),
                        "actual_closing_price" => $value->Actual,
                        "pred_closing_price" => $value->Predict
                    ]);
                }
            }
            else if($coin == 'ethereum'){
                Ethereum::truncate();
                foreach ($jsonResult->ethereum as $key => $value) {
                    Ethereum::create([
                        "date" => $value->Date,
                        "actual_closing_price" => $value->Actual,
                        "pred_closing_price" => $value->Predict
                    ]);
                }
            }
            else {
                XRP::truncate();
                foreach ($jsonResult->xrp as $key => $value) {
                    XRP::create([
                        "date" => $value->Date,
                        "actual_closing_price" => $value->Actual,
                        "pred_closing_price" => $value->Predict
                    ]);
                }
            }

            return $jsonResult;
        }
        else{
            return 'No value';
        }
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
    }
}
