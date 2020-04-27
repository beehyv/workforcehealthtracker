/*
 *  Licensed to the Apache Software Foundation (ASF) under one
 *  or more contributor license agreements.  See the NOTICE file
 *  distributed with this work for additional information
 *  regarding copyright ownership.  The ASF licenses this file
 *  to you under the Apache License, Version 2.0 (the
 *  "License"); you may not use this file except in compliance
 *  with the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing,
 *  software distributed under the License is distributed on an
 *  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 *  KIND, either express or implied.  See the License for the
 *  specific language governing permissions and limitations
 *  under the License.
 *
 *  Built and managed with Open Source Love by BeeHyv Software Solutions Pvt Ltd. Hyderabad
 *  www.beehyv.com
 */

export const actions = language => [
  {
    id: 1,
    result_status: language.no_action,
    result_message: language.no_action,
    color: '#444444'
  },
  {
    id: 3,
    result_status: language.results_pending,
    result_message: language.results_pending,
    color: '#444444'
  },
  {
    id: 4,
    result_status: language.tested_negative,
    result_message: language.tested_negative,
    color: '#e60000'
  },
  {
    id: 5,
    result_status: language.tested_positive,
    result_message: language.tested_positive,
    color: '#4cbb17'
  },
  {
    id: 6,
    result_status: language.test_ordered,
    result_message: language.test_ordered,
    color: '#444444'
  },
  {
    id: 7,
    result_status: language.home_quarantine_symptom,
    result_message: language.home_quarantine_symptom_message,
    color: '#f76a14'
  },
  {
    id: 8,
    result_status: language.precaution_measure_symptom,
    result_message: language.precaution_measure_symptom_message,
    color: '#ffb366'
  },
  {
    id: 9,
    result_status: language.home_quarantine_general,
    result_message: language.home_quarantine_general_message,
    color: '#f76a14'
  },
  {
    id: 10,
    result_status: language.precaution_measure_general,
    result_message: language.precaution_measure_general_message,
    color: '#f76a14'

  },
  {
    id: 11,
    result_status: language.advise_to_stay_home,
    result_message: language.advise_to_stay_home_message,
    color: '#f76a14'

  }
];
