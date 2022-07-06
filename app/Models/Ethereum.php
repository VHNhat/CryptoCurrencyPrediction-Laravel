<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Ethereum extends Model
{
    use HasFactory;
    public $table = 'ethereum';
    protected $fillable = ['date', 'actual_closing_price', 'pred_closing_price'];
    public $timestamps = false;
}
