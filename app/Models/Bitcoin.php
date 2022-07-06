<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Bitcoin extends Model
{
    use HasFactory;
    protected  $table = 'bitcoin';
    protected $fillable = ['date', 'actual_closing_price', 'pred_closing_price'];
    public $timestamps = false;
}
