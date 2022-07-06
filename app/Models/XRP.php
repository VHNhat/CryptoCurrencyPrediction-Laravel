<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class XRP extends Model
{
    use HasFactory;
    public $table = 'xrp';
    protected $fillable = ['date', 'actual_closing_price', 'pred_closing_price'];
    public $timestamps = false;
}
